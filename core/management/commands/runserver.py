import json

from django.core.management import CommandError
from django.core.management.commands.runserver import Command as RunServerCommand

from core.services.vm_attack_service import vm_attack_service


class Command(RunServerCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--vm_file', help='Path to file that will be used to generate customer\'s virtual structure.', type=str,
        )

    def handle(self, *args, **options):
        vm_filename = options.get('vm_file')
        if vm_filename is None:
            raise CommandError('To start service provide --vm_file')

        self.setup_attack_service(vm_filename)

        super().handle(*args, **options)

    def setup_attack_service(self, filename):
        with open(filename, 'r') as json_file:
            vm_structure = json.load(json_file)

            if 'vms' not in vm_structure or 'fw_rules' not in vm_structure:
                raise CommandError('Wrong file provided to --vm_file')

            vm_attack_service.set_cloud_environment(vm_structure['vms'], vm_structure['fw_rules'])
