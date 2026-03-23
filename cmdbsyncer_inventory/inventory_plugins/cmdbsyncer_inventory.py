# inventory_plugins/my_rest_plugin.py
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.errors import AnsibleError
from ansible.utils.display import Display
import requests
import os



DOCUMENTATION = r'''
    name: cmdbsyncer_inventory
    plugin_type: inventory
    short_description: Inventory Plugin for Cmdbsyncer Data
    description:
      - Reads the dynamic inventory from Cmdbsyncer
    options:
      plugin:
        description: Cmdbsyncer Inventory
        required: true
        choices: ['cmdbsyncer_inventory']
      api_url:
        description: Url to the Cmdbsyncer
        required: true
        type: string
      username:
        description: Username
        required: false
        type: string
      password:
        description: Password
        required: false
        type: string
      verify_ssl:
        description: Verify SSL certificates
        required: false
        type: bool
        default: true
'''

class InventoryModule(BaseInventoryPlugin):
    NAME = 'cmdbsyncer_inventory'
    #display = Display()
    def verify_file(self, path):
        #valid = super(InventoryModule, self).verify_file(path)
        #if not valid:
        #   return False
        #return self.get_option('plugin') == self.NAME
        valid = super().verify_file(path)
        if not valid:
            return False
        return path.endswith(('.yml', '.yaml'))


    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)
        display = Display()
        self._read_config_data(path)
        api_url  = self.get_option('api_url')
        username = os.environ.get("CMDBSYNCER_APIUSER")
        password = os.environ.get("CMDBSYNCER_APIPASSWORD")

        display.warning(
            f"ENV DEBUG: CMDBSYNCER_APIUSER present={bool(username)}, "
            f"CMDBSYNCER_APIPASSWORD present={bool(password)}"
        )

        if not username or not password:
            username = self.get_option('username')
            password = self.get_option('password')
        
        verify_ssl = self.get_option('verify_ssl')
        api_url += "/api/v1/ansible/"

        

        try:
            headers = {
                'x-login-user': f'{username}:{password}'
            }
            resp = requests.get(
                api_url,
                headers=headers,
                timeout=10,
                verify=verify_ssl,
            )
        except Exception as e:
            raise AnsibleError("Error during REST API call: %s" % e)

        if resp.status_code != 200:
            raise AnsibleError(
                "REST API responded with status %s" % resp.status_code
            )

        



        data = resp.json()
        self._populate_from_api(data)

    def _populate_from_api(self, data):
        """
        Parse traditional Ansible inventory format from cmdbsyncer API
        
        Example traditional format:
            >>> data = {
            ...     "_meta": {
            ...         "hostvars": {
            ...             "web1.example.com": {
            ...                 "ansible_host": "10.0.0.1",
            ...                 "ansible_user": "ec2-user",
            ...                 "ansible_groups": ["web", "linux"]
            ...             }
            ...         }
            ...     },
            ...     "all": {
            ...         "hosts": ["web1.example.com"]
            ...     }
            ... }
        """
        all_hosts = data.get('all', {}).get('hosts', [])
        hostvars = data.get('_meta', {}).get('hostvars', {})
        
        # Process each host
        for hostname in all_hosts:
            self.inventory.add_host(hostname)
            host_vars = hostvars.get(hostname, {})
            
            groups = host_vars.pop('ansible_groups', ['ungrouped'])
            if not isinstance(groups, list):
                groups = [groups] if groups else ['ungrouped']
            
            # Set host variables
            for key, value in host_vars.items():
                self.inventory.set_variable(hostname, key, value)
            
            # Create groups and assign host to them
            for group_name in groups:
                if not self.inventory.groups.get(group_name):
                    self.inventory.add_group(group_name)
                self.inventory.add_host(hostname, group=group_name)