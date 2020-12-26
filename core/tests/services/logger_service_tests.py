import random
from unittest import TestCase

from core.services.logger_service import logger


class LoggerServiceTest(TestCase):
    REQUEST_AVG_TIME = 0.200

    def setUp(self):
        self.logger = logger
        self.logger._requests_count = 0
        self.logger._full_request_time = 0

    def test_log(self):
        logger.log_request_time(self.REQUEST_AVG_TIME)

        self.assertEqual(1, logger.get_requests_count())
        self.assertEqual(self.REQUEST_AVG_TIME, logger.get_average_request_time())

    def test_requests_count(self):
        for _ in range(100):
            logger.log_request_time(self.REQUEST_AVG_TIME)

        self.assertEqual(100, logger.get_requests_count())

    def test_average_request_time(self):
        full_time = 0

        for _ in range(100):
            request_time = random.random()
            full_time += request_time
            logger.log_request_time(request_time)

        self.assertEqual(full_time / 100, logger.get_average_request_time())
