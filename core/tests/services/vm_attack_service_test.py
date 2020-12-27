import json
from unittest import TestCase

from core.services.vm_attack_service import vm_attack_service


class VmAttackServiceTest(TestCase):
    vm_file_spec = 'core/tests/fixtures/input-0.json'

    @classmethod
    def setUpClass(cls) -> None:
        with open(cls.vm_file_spec, 'r') as json_file:
            vm_structure = json.load(json_file)
            vm_attack_service.set_cloud_environment(vm_structure['vms'], vm_structure['fw_rules'])
