import json
from unittest import TestCase

from core.services.vm_attack_service import vm_attack_service, VmAttackServiceSetUpException, VmAttackService


class VmAttackServiceTest(TestCase):
    # Different fixtures
    vm_input_0 = 'core/tests/fixtures/input-0.json'
    vm_input_1 = 'core/tests/fixtures/input-1.json'
    vm_input_2 = 'core/tests/fixtures/input-2.json'
    vm_input_3 = 'core/tests/fixtures/input-3.json'
    vm_input_4 = 'core/tests/fixtures/input-4.json'

    def _load_json_file(self, filename):
        with open(filename, 'r') as json_file:
            return json.load(json_file)

    def _upload_vm_file_to_service(self, filename):
        data = self._load_json_file(filename)
        vm_attack_service.set_cloud_environment(data['vms'], data['fw_rules'])

    def test_wrong_file_structure_input(self):
        data = self._load_json_file(self.vm_input_4)

        with self.assertRaises(VmAttackServiceSetUpException):
            vm_attack_service.set_cloud_environment(data['vms'], data['fw_rules'])

        with self.assertRaises(VmAttackServiceSetUpException):
            vm_attack_service._validate_vms(data['vms'])

        with self.assertRaises(VmAttackServiceSetUpException):
            vm_attack_service._validate_fw_rules(data['fw_rules'])

    def test_success_validation(self):
        # Check for no exceptions
        for filename in [self.vm_input_0, self.vm_input_1, self.vm_input_2, self.vm_input_3]:
            self._upload_vm_file_to_service(filename)
            self._check_service_is_ready()

    def _check_service_is_ready(self):
        self.assertEqual(True, vm_attack_service._validated)
        self.assertNotEqual(0, vm_attack_service._vm_count)
        self.assertNotEqual([], vm_attack_service._graph)

    def test_generate_graph(self):
        # Input 1
        self._upload_vm_file_to_service(self.vm_input_1)
        expected = [set(), set(), set(), set(), set(), set(), set(), set(), set(), set()]
        self.assertListEqual(expected, vm_attack_service._graph)

        # Input 2
        self._upload_vm_file_to_service(self.vm_input_2)
        expected = [{0, 1, 2, 3, 4}] * 5
        self.assertListEqual(expected, vm_attack_service._graph)

    def test_get_all_vulnerable_vm_id(self):
        self._upload_vm_file_to_service(self.vm_input_3)
        vulnerable_vm = vm_attack_service.get_all_vulnerable_vm_id('vm-9ea3998')
        expected = ['vm-9ea3998', 'vm-ab51cba10']
        self.assertListEqual(expected, vulnerable_vm)

        vulnerable_vm = vm_attack_service.get_all_vulnerable_vm_id('vm-a3660c')
        expected = ['vm-a3660c', 'vm-ab51cba10']
        self.assertListEqual(expected, vulnerable_vm)

        vm_attack_service.get_all_vulnerable_vm_id('vm-2987241')
        expected = ['vm-a3660c', 'vm-ab51cba10']
        self.assertListEqual(expected, vulnerable_vm)
