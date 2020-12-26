class Logger:
    """Logger that logs count of requests, average response time"""

    _requests_count = 0
    _full_request_time = 0

    def log(self, request_time: float):
        """Log request"""
        pass

    def get_requests_count(self):
        return

    def get_average_request_time(self):
        pass


logger = Logger()
