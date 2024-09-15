from common.kafka_producer import send_message
from common.config import settings
from common.time_giver import TimeGiver
from kafka.producer import producer
from functions.schedule import get_future_schedules, overdue_schedule, check_all_resolved
from functions.agreement import get_agreement_by_id, get_new_agreements


async def send_to_orig():
    agreements = await get_new_agreements()
    for agr in agreements:
        async with producer.session() as session:
            await send_message(session, settings.kafka_agreement_topic, {"client_id": agr.client_id,
                                                                             "disbursment_amount": agr.principal_amount - agr.origination_amount,
                                                                             "agreement_id": agr.id,
                                                                             "product_code": agr.product_code})

time_giver = TimeGiver()


async def check_dates():
    schedules = await get_future_schedules()
    time = time_giver.get_current_time()
    for sch in schedules:
        if sch.payment_date < time:
            await overdue_schedule(sch.id)
            agreement = await get_agreement_by_id(sch.agreement_id)
            async with producer.session() as session:
                await send_message(session, settings.kafka_overdue_payment_topic, {"customer_id": agreement.client_id,
                                                                                   "agreement_id": sch.agreement_id,
                                                                                   "overdue_date": time.isoformat(),
                                                                                   "payment": sch.principal_payment})
            await check_all_resolved({"agreement_id": sch.agreement_id})
