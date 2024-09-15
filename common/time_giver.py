from datetime import datetime
from common.config import settings


class TimeGiver:
    def __init__(self):
        self.time = settings.time_testing_value
        self.test = settings.time_testing

    def get_current_time(self):
        if self.test:
            return self.time
        else:
            return datetime.now()
