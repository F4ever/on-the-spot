from django.http import JsonResponse
from django.views.decorators.http import require_GET

from core.services.logger_service import logger_service
from core.services.vm_attack_service import vm_attack_service


@require_GET
def stats_view(request):
    response_data = {
        'vm_count': vm_attack_service.get_vm_count(),
        'request_count': logger_service.get_requests_count(),
        'average_request_time': logger_service.get_average_request_time(),
    }

    return JsonResponse(data=response_data)


@require_GET
def attack_view(request):
    pass
