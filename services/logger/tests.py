import random

from django.test import TestCase

from services.logger.logger_service import logger


class LoggerServiceTestCase(TestCase):
    REQUEST_AVG_TIME = 0.200

    def setUp(self):
        self.logger = logger
        self.logger._requests_count = 0
        self.logger._full_request_time = 0

    def test_log(self):
        logger.log(self.REQUEST_AVG_TIME)

        self.assertEqual(1, logger.get_requests_count())
        self.assertEqual(self.REQUEST_AVG_TIME, logger.get_average_request_time())

    def test_requests_count(self):
        for _ in range(100):
            logger.log(self.REQUEST_AVG_TIME)

        self.assertEqual(100, logger.get_requests_count())

    def test_average_request_time(self):
        full_time = 0

        for _ in range(100):
            request_time = random.random()
            full_time += request_time
            logger.log(request_time)

        self.assertEqual(full_time / 100, logger.get_average_request_time())