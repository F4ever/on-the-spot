from unittest import TestCase

from django.test import Client

from core.services.vm_attack_service import vm_attack_service


class StatsApiTest(TestCase):
    url = '/api/v1/stats/'

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = Client()
        vm_attack_service.set_cloud_environment([], [])

    def test_stats_success(self):
        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.json()['vm_count'])
        self.assertEqual(0, response.json()['request_count'])
        self.assertEqual(0, response.json()['average_request_time'])

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.json()['vm_count'])
        self.assertEqual(1, response.json()['request_count'])
