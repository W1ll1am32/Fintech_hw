import json
from common.kafka_consumer import KafkaConsumerSessionManager
from common.config import settings
from functions.agreement import update_agreement
from functions.schedule import add_schedule, pay_schedule, check_all_resolved

consumer = KafkaConsumerSessionManager({"bootstrap_servers": f"{settings.kafka_host}:{settings.kafka_port}",
                                        "group_id": f"{settings.kafka_pe_scoring_consumer_group}",
                                        "auto_offset_reset": 'earliest'})
consumer_payment = KafkaConsumerSessionManager({"bootstrap_servers": f"{settings.kafka_host}:{settings.kafka_port}",
                                                 "group_id": f"{settings.kafka_pe_schedule_consumer_group}",
                                                 "auto_offset_reset": 'earliest'})


async def create_schedule(msg: bytes):
    data = json.loads(msg.value.decode("ascii"))
    await update_agreement(data)
    await add_schedule(data["agreement_id"])


async def payment_schedule(msg: bytes):
    data = json.loads(msg.value.decode("ascii"))
    await pay_schedule(data)
    await check_all_resolved(data)
