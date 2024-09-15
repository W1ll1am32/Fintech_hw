import json
from common.kafka_consumer import KafkaConsumerSessionManager
from common.config import settings
from functions.application import check_and_create, update_application
from models.dto.models import InputModel

consumer_pe = KafkaConsumerSessionManager({"bootstrap_servers": f"{settings.kafka_host}:{settings.kafka_port}",
                                           "group_id": f"{settings.kafka_origination_agreement_consumer_group}",
                                           "auto_offset_reset": 'earliest'})
consumer_scoring = KafkaConsumerSessionManager({"bootstrap_servers": f"{settings.kafka_host}:{settings.kafka_port}",
                                                "group_id": f"{settings.kafka_origination_scoring_consumer_group}",
                                                "auto_offset_reset": 'earliest'})


async def create_application(msg: bytes):
    data = json.loads(msg.value.decode("ascii"))
    await check_and_create(InputModel.from_dict(data))


async def change_status(msg: bytes):
    data = json.loads(msg.value.decode("ascii"))
    await update_application({"application_id": data["application_id"], "field": "status", "value": data["status"]})
