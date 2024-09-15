import json
from common.kafka_consumer import KafkaConsumerSessionManager
from common.config import settings
from functions.scoring import score

consumer = KafkaConsumerSessionManager({"bootstrap_servers": f"{settings.kafka_host}:{settings.kafka_port}",
                                        "group_id": f"{settings.kafka_scoring_consumer_group}",
                                        "auto_offset_reset": 'earliest'})


async def scoring(msg: bytes):
    data = json.loads(msg.value.decode("ascii"))
    await score(data)
