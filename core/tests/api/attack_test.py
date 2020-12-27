import json
from unittest import TestCase

from django.test import Client

from core.services.vm_attack_service import vm_attack_service


class AttackApiTest(TestCase):
    url = '/api/v1/attack/'
    vm_file_spec = 'core/tests/fixtures/input-0.json'

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = Client()

        with open(cls.vm_file_spec, 'r') as json_file:
            vm_structure = json.load(json_file)
            vm_attack_service.set_cloud_environment(vm_structure['vms'], vm_structure['fw_rules'])

    def test_attack_without_param(self):
        response = self.client.get(self.url)

        self.assertEqual(400, response.status_code)
        self.assertIn('error', response.json())

    def test_attack_success(self):
        response = self.client.get(self.url, {'vm_id': 'vm-c7bac01a07'})

        self.assertEqual(200, response.status_code)
        self.assertIn('vm-a211de', response.json())
        self.assertIn('vm-c7bac01a07', response.json())

        response = self.client.get(self.url, {'vm_id': 'vm-a211de'})

        self.assertEqual(200, response.status_code)
        self.assertIn('vm-a211de', response.json())
        self.assertNotIn('vm-c7bac01a07', response.json())

    def test_attack_with_wrong_vm_id(self):
        response = self.client.get(self.url, {'vm_id': 'some_id'})

        self.assertEqual(400, response.status_code)
        self.assertIn('error', response.json())
        self.assertEqual('There is no vm with id: [some_id].', response.json()['error'])
