class LoggerService:
    """Logger that logs count of requests, average response time"""

    _requests_count = 0
    _full_request_time = 0

    def log_request_time(self, request_time: float):
        """Log request average time"""
        self._requests_count += 1
        self._full_request_time += request_time

    def get_requests_count(self):
        return self._requests_count

    def get_average_request_time(self):
        """Returns average request execution time"""
        if self._requests_count == 0:
            return 0

        return self._full_request_time / self._requests_count


logger_service = LoggerService()
