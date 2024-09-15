from common.kafka_producer import send_message
from common.config import settings
from kafka.producer import producer
from functions.application import get_new_applications, update_application


async def send_to_scoring():
    applications_id = await get_new_applications()
    if len(applications_id) != 0:
        for app_id in applications_id:
            application = await update_application({"application_id": app_id, "field": "status", "value": "SCORING"})
            async with producer.session() as session:
                await send_message(session, settings.kafka_scoring_topic, {"application_id": app_id,
                                                                           "client_id": application.client_id,
                                                                           "agreement_id": application.agreement_id})
