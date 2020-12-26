from django.http import JsonResponse
from django.views.decorators.http import require_GET

from core.services.logger_service import logger_service
from core.services.vm_attack_service import vm_attack_service, VmAttackServiceException


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
    vm_id = request.GET.get('vm_id')

    if vm_id is None:
        return JsonResponse(data={'error': 'Fill "vm_id" param'}, status=400)

    try:
        vulnerable_vms = vm_attack_service.get_all_vulnerable_vm(vm_id)
    except VmAttackServiceException as error:
        return JsonResponse(data={'error': error}, status=400)

    return JsonResponse(data=vulnerable_vms)
