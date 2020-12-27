from collections import defaultdict
from typing import List, Dict, Union

from schema import Schema, SchemaError


class VmAttackServiceSetUpException(Exception):
    pass


class VmAttackServiceException(Exception):
    pass


class VmAttackService:
    """
        Service that shows vulnerable virtual machines in customers env.
    """
    _validated = False

    _vms = []
    _fw_rules = []
    _vm_count = 0

    _tag_owners = defaultdict(list)
    _graph = []

    def set_cloud_environment(
            self,
            vms: List[Dict[str, Union[str, List[str]]]],
            fw_rules: List[Dict[str, str]],
    ):
        """
            Setup clients vm and firewall rules. Create the graph for fast calculations.
            vms - List of virtual machines on clients side.
            example:
            {
                "vm_id": "vm-xxxxxxx",
                "name": "jira server",
                "tags": ["tag1", ..],
            }
            fw_rules - List of rules that one vm can access another
            example:
            {
                "fw_id": "fw-xxxxx",
                "source_tag": "tag1",
                "dest_tag": "tag2"
            }
            :raises VmAttackServiceSetUpException if setup was incorrect
        """
        # Validate data
        self._validate_data(vms, fw_rules)

        # Store data
        self._vms = vms
        self._fw_rules = fw_rules
        self._vm_count = len(vms)

        # Generate graph
        self._generate_tag_owners()
        self._generate_vertexes()
        self._generate_ribs()

    def _validate_data(self, vms, fw_rules):
        """Validating big python structures"""
        self._validate_vms(vms)
        self._validate_fw_rules(fw_rules)
        self._validated = True

    def _validate_vms(self, vms):
        vms_validate_schema = Schema([{
            'vm_id': str,
            'name': str,
            'tags': [str],
        }])

        try:
            vms_validate_schema.validate(vms)
        except SchemaError as error:
            raise VmAttackServiceSetUpException(f'Wrong vms data structure. More: [{error}]')

    def _validate_fw_rules(self, fw_rules):
        fw_rules_validate_schema = Schema([{
            'fw_id': str,
            'source_tag': str,
            'dest_tag': str,
        }])

        try:
            fw_rules_validate_schema.validate(fw_rules)
        except SchemaError as error:
            raise VmAttackServiceSetUpException(f'Wrong vms data structure. More: [{error}]')

    def _generate_tag_owners(self):
        """Generate dict where key is Tag name, value is list of machines that has this tag"""
        for index, vm in enumerate(self._vms):
            for tag in vm['tags']:
                self._tag_owners[tag].append(index)

    def _generate_vertexes(self):
        """
            First of all lets try to create adjacency matrix.
            All vms are graph vertices and fw_rules are ribs.
            Index in list vms will be their id in matrix.
        """
        # generate list of sets for each vms
        self._graph = [set() for _ in range(self._vm_count)]

    def _generate_ribs(self):
        """Each rib will be a 1 in matrix"""
        for fw in self._fw_rules:
            source_tag = fw['source_tag']
            dest_tag = fw['dest_tag']

            for source_vm_index in self._tag_owners[source_tag]:
                for dest_vm_index in self._tag_owners[dest_tag]:
                    # Add to each vertex access ability nodes
                    self._graph[source_vm_index].add(dest_vm_index)

    def get_all_vulnerable_vm_id(self, vm_id: str) -> List[str]:
        """vm_id - virtual machine id that will be used as entry point for attacker."""
        attacker_vm_index = self._get_vm_index(vm_id)

        # Go through the graph
        indexes = self._get_all_accessible_vertex_from_index(attacker_vm_index)

        # Return only vm ids
        return [self._vms[index]['vm_id'] for index in indexes]

    def _get_vm_index(self, vm_id: str) -> int:
        """Try to find index of provided vm. Exception if there is no vm with such id."""
        for index, vm in enumerate(self._vms):
            if vm['vm_id'] == vm_id:
                return index

        raise VmAttackServiceException(f'There is no vm with id: [{vm_id}].')

    def _get_all_accessible_vertex_from_index(self, index: int) -> List[int]:
        """Depth-first graph traversal algorithm"""
        # The index is the first one vertex
        visited_vertex = [index]
        vertex_to_visit = [index]

        while True:
            # Get next vertex to visit
            current_vertex = vertex_to_visit.pop()
            # Iterate over all vertexes that we can visit
            for vertex in self._graph[current_vertex]:
                if vertex not in visited_vertex:
                    visited_vertex.append(vertex)
                    vertex_to_visit.append(vertex)

            if not vertex_to_visit:
                break

        return visited_vertex

    @property
    def vm_count(self) -> int:
        return self._vm_count


vm_attack_service = VmAttackService()
