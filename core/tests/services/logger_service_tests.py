import random
from unittest import TestCase

from core.services.logger_service import logger_service


class LoggerServiceTest(TestCase):
    REQUEST_AVG_TIME = 0.200

    def setUp(self):
        self.logger = logger_service
        self.logger._requests_count = 0
        self.logger._full_request_time = 0

    def test_log(self):
        logger_service.log_request_time(self.REQUEST_AVG_TIME)

        self.assertEqual(1, logger_service.get_requests_count())
        self.assertEqual(self.REQUEST_AVG_TIME, logger_service.get_average_request_time())

    def test_requests_count(self):
        for _ in range(100):
            logger_service.log_request_time(self.REQUEST_AVG_TIME)

        self.assertEqual(100, logger_service.get_requests_count())

    def test_average_request_time(self):
        full_time = 0

        for _ in range(100):
            request_time = random.random()
            full_time += request_time
            logger_service.log_request_time(request_time)

        self.assertEqual(full_time / 100, logger_service.get_average_request_time())
