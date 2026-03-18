#!/usr/bin/env python3
"""
Entry point for running cmdbsyncer_inventory as a module.
Usage: python -m cmdbsyncer_inventory
"""

from . import install_plugin

if __name__ == "__main__":
    print("🔧 CMDBSyncer Inventory Plugin Installer")
    print("=" * 50)
    success = install_plugin()
    if success:
        exit(0)
    else:
        exit(1)