from datetime import datetime

from django.utils.deprecation import MiddlewareMixin

from core.services.logger_service import logger_service


class LoggerMiddleware(MiddlewareMixin):
    """Logging request time via LoggerService"""

    def process_request(self, request):
        request._start_dt = datetime.now()

    def process_response(self, request, response):
        response_time = (datetime.now() - request._start_dt).total_seconds()
        logger_service.log_request_time(response_time)
        return response
