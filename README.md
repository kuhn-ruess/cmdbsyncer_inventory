# cmdbsyncer_inventory
Ansible Inventory Plugin for Cmdbsyncer


## Example File Strucutre

./ansible.cfg
/collections/ansible_collections/kuhn_ruess/cmdbsyncer_inv/galaxy.yml
/collections/ansible_collections/kuhn_ruess/cmdbsyncer_inv/plugins/inventory/cmdbsyncer_inventory.py (the Plugin)
/inventory/inventory.yml (config with url)

### Example ansible.cfg

```
[defaults]
collections_path = ./collections


[inventory]
enable_plugins = host_list, script, auto, yaml, ini, toml, kuhn_ruess.cmdbsyncer_inv.cmdbsyncer_inventory
```
