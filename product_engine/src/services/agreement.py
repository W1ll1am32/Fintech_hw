from fastapi import Depends
from models.dao.orm_models import Agreement, Client, Product
from models.dto.models import AgreementModel, FormModel, ClientModel, ProductModel
from random import randint
from kafka.producer import get_producer
from common.kafka_producer import send_message
from common.config import settings
from common.repository_getter import get_repository
from services.client import ClientService
from services.product import ProductService


class AgreementService:
    def __init__(self, agreement_repo=Depends(get_repository(Agreement)),
                 client_service: ClientService = Depends(ClientService),
                 product_service: ProductService = Depends(ProductService),
                 producer=Depends(get_producer)):
        self._agreement_repo = agreement_repo
        self._client_service = client_service
        self._product_service = product_service
        self._producer = producer

    async def get_agreements(self):
        agreements = await self._agreement_repo.get_all()
        return [AgreementModel.from_dao(x) for x in agreements]

    async def get_agreements_by_id(self, id: int):
        agreement = await self._agreement_repo.get_by_id(id)
        if agreement is not None:
            return AgreementModel.from_dao(agreement)
        return None

    async def get_agreements_by_client_id(self, client_id: int):
        check = await self._client_service.get_client_by_id(client_id)
        if check is None:
            return None
        agreements = await self._agreement_repo.get_by_field('client_id', client_id)
        if len(agreements) != 0:
            return [(AgreementModel.from_dao(x), x.id) for x in agreements]
        return []

    async def create_agreement(self, form: FormModel):
        product = await self._product_service.get_product_by_code(form.product_code)
        if product is None:
            return None, None, 404

        origination_amount = randint(product.min_origination_amount, product.max_origination_amount)
        principal_amount = form.disbursment_amount + origination_amount

        if not (product.min_term <= form.term <= product.max_term and
                product.min_interest <= form.interest <= product.max_interest and
                product.min_principal_amount <= principal_amount <= product.max_principal_amount):
            return None, None, 400

        list = [getattr(form, column) for column in form.model_fields.keys() if
                column != 'product_code' and column != 'term' and column != 'interest' and column != 'disbursment_amount']
        try:
            client = await self._client_service.get_and_create(list, form)
        except:
            return None, None, 409
        client_id = client.id

        agreement = AgreementModel.from_form(form)
        agreement.client_id = client_id
        agreement.principal_amount = principal_amount
        agreement.origination_amount = origination_amount
        agreement_dao = await self._agreement_repo.add(Agreement.from_dto(agreement))

        try:
            await send_message(self._producer, settings.kafka_agreement_topic, {"client_id": agreement_dao.client_id,
                                                                            "disbursment_amount": form.disbursment_amount,
                                                                            "agreement_id": agreement_dao.id,
                                                                            "product_code": agreement_dao.product_code})
        except:
            print("Kafka not available")
            return None, None, 503

        return agreement_dao.id, agreement_dao.client_id, 200
