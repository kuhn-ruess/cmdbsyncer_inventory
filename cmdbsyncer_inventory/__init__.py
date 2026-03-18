"""
CMDBSyncer Inventory Plugin for Ansible

A dynamic Ansible inventory plugin that fetches host and group information from CMDBSyncer.
"""

__version__ = "0.1.0"
__author__ = "Bastian Kuhn"
__email__ = "bastian.kuhn@kuhn-ruess.de"

import os
import shutil
import sys
from pathlib import Path

def install_plugin():
    """
    Install the plugin to make it available for Ansible.
    This function creates a symlink or copies the plugin to a location where Ansible can find it.
    """
    import ansible
    
    # Get the plugin source file
    plugin_source = Path(__file__).parent / "inventory_plugins" / "cmdbsyncer_inventory.py"
    
    if not plugin_source.exists():
        print(f"❌ Plugin source not found: {plugin_source}")
        return False
    
    # Try multiple potential Ansible plugin directories
    ansible_dir = Path(ansible.__file__).parent
    potential_dirs = [
        ansible_dir / "plugins" / "inventory",
        Path.home() / ".ansible" / "plugins" / "inventory",
    ]
    
    # Create ~/.ansible/plugins/inventory as fallback
    fallback_dir = Path.home() / ".ansible" / "plugins" / "inventory"
    fallback_dir.mkdir(parents=True, exist_ok=True)
    potential_dirs.append(fallback_dir)
    
    installed = False
    for target_dir in potential_dirs:
        if target_dir.exists() or target_dir == fallback_dir:
            target_file = target_dir / "cmdbsyncer_inventory.py"
            try:
                shutil.copy2(plugin_source, target_file)
                print(f"✅ Plugin installed to: {target_file}")
                installed = True
                break
            except PermissionError:
                print(f"⚠️  Permission denied for: {target_dir}")
                continue
            except Exception as e:
                print(f"⚠️  Failed to install to {target_dir}: {e}")
                continue
    
    if not installed:
        print("❌ Could not install plugin to any Ansible directory")
        print("💡 Manual installation needed:")
        print(f"   Copy {plugin_source}")
        print("   To your project's inventory_plugins/ directory")
        return False
    
    print("🎉 Plugin installation complete!")
    print("You can now use: plugin: cmdbsyncer_inventory in your inventory files")
    return True

# Make the plugin discoverable by Ansible
def get_inventory_plugins():
    """Return list of inventory plugins provided by this package."""
    return ["cmdbsyncer_inventory.inventory_plugins.cmdbsyncer_inventory"]