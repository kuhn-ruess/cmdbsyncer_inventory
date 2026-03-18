# CMDBSyncer Inventory Plugin

[![PyPI version](https://badge.fury.io/py/cmdbsyncer-inventory.svg)](https://badge.fury.io/py/cmdbsyncer-inventory)
[![Python Support](https://img.shields.io/pypi/pyversions/cmdbsyncer-inventory.svg)](https://pypi.org/project/cmdbsyncer-inventory/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An Ansible dynamic inventory plugin that fetches host and group information from CMDBSyncer.

## Installation

### Via pip (Recommended)

```bash
# Install the package
pip install cmdbsyncer-inventory

# Auto-install plugin for Ansible (run once after installation)
python -m cmdbsyncer_inventory
```

**That's it!** The plugin is now automatically available to Ansible. 

### Alternative methodm

**Method 1: Using the install command (if available)**
```bash
cmdbsyncer-install-plugin  # If console scripts work on your system
```

**Method 2: Manual copy to project** 
```bash
# Install the package
pip install cmdbsyncer-inventory

# Manually copy to your project
mkdir -p inventory_plugins
python -c "
import cmdbsyncer_inventory
from pathlib import Path
import shutil

src = Path(cmdbsyncer_inventory.__file__).parent / 'inventory_plugins' / 'cmdbsyncer_inventory.py'
shutil.copy2(src, 'inventory_plugins/cmdbsyncer_inventory.py')
print('Plugin copied to ./inventory_plugins/')
"
```

### Via pip from source

```bash
pip install git+https://github.com/kuhn-ruess/cmdbsyncer-inventory.git
python -m cmdbsyncer_inventory
```

## Usage

After installation and running `python -m cmdbsyncer_inventory`, the plugin is automatically available to Ansible. You just need to:

1. **Create an inventory configuration file** (e.g., `inventory.yml`):

```yaml
plugin: cmdbsyncer_inventory
api_url: https://your-cmdbsyncer-instance.com
username: your_username  # Optional if using environment variables
password: your_password  # Optional if using environment variables
```

2. **Set environment variables** (recommended for credentials):

```bash
export CMDBSYNCER_APIUSER="your_username"
export CMDBSYNCER_APIPASSWORD="your_password"
```

3. **Use with ansible commands**:

```bash
# Test the inventory
ansible-inventory -i inventory.yml --list

# Run playbooks
ansible-playbook -i inventory.yml your-playbook.yml
```

**Note**: No `ansible.cfg` configuration needed after automatic installation!

## Configuration Options

| Option | Required | Type | Description |
|--------|----------|------|-------------|
| `plugin` | Yes | string | Must be `cmdbsyncer_inventory` |
| `api_url` | Yes | string | URL to your CMDBSyncer instance |
| `username` | No | string | API username (can use `CMDBSYNCER_APIUSER` env var) |
| `password` | No | string | API password (can use `CMDBSYNCER_APIPASSWORD` env var) |

## Example Output

The plugin will create Ansible inventory with hosts and groups based on your CMDBSyncer configuration. Example structure:

```json
{
  "_meta": {
    "hostvars": {
      "server1.example.com": {
        "ansible_host": "10.0.0.1",
        "ansible_user": "admin",
        "environment": "production"
      }
    }
  },
  "production": {
    "hosts": ["server1.example.com"]
  },
  "web": {
    "hosts": ["server1.example.com"]  
  }
}
```

## Requirements

- Python 3.7+
- Ansible Core 2.12+
- CMDBSyncer instance with API access

## Development

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/kuhn-ruess/cmdbsyncer-inventory.git
cd cmdbsyncer-inventory

# Install in development mode
pip install -e .

# Install plugin for Ansible
python -m cmdbsyncer_inventory

# Test the plugin
ansible-inventory -i example-inventory.yml --list
```

### Building for PyPI

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- � Email: info@kuhn-ruess.de
- �🐛 Issues: [GitHub Issues](https://github.com/kuhn-ruess/cmdbsyncer-inventory/issues)
- 📖 Documentation: [Wiki](https://github.com/kuhn-ruess/cmdbsyncer-inventory/wiki)
