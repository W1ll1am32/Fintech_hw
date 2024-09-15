from pydantic_settings import BaseSettings
from datetime import datetime, timedelta


class Settings(BaseSettings):
    application_delay: int = 59
    job_send_to_orig_seconds: int = 59 * 3
    job_check_dates_seconds: int = 59   # 86400
    job_send_to_scoring_seconds: int = 59
    product_engine_host: str = 'product_engine'
    product_engine_port: int = 8000
    origination_host: str = 'origination'
    origination_port: int = 8001
    gateway_host: str = 'gateway'
    gateway_port: int = 8002
    scoring_host: str = 'scoring'
    scoring_port: int = 8003
    kafka_host: str = 'kafka'
    kafka_port: int = 29092
    kafka_agreement_topic: str = 'new-agreements'
    kafka_scoring_topic: str = 'scoring-request'
    kafka_scoring_response_topic: str = 'scoring-response'
    kafka_schedule_payment_topic: str = 'payment-received'
    kafka_overdue_payment_topic: str = 'payment-overdue'
    kafka_pe_scoring_consumer_group: str = 'pe-consumer'
    kafka_origination_agreement_consumer_group: str = 'agreement-consumer'
    kafka_origination_scoring_consumer_group: str = 'orig-consumer'
    kafka_pe_schedule_consumer_group: str = 'schedule-consumer'
    kafka_scoring_consumer_group: str = 'scoring-consumer'
    time_testing: bool = True
    time_testing_value: datetime = datetime.now() + timedelta(days=300)


settings = Settings()
