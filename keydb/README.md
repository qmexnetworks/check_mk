# KeyDB

A CheckMK plugin for [KeyDB](https://docs.keydb.dev/) based on the [Redis Plugin by CheckMK](https://github.com/tribe29/checkmk).

## Installation

- Move `bakery/keydb.py` to your Check_MK bakery directory: `/omd/sites/<SITE>/local/lib/check_mk/base/cee/plugins/bakery/keydb.py`
    - This file will let the Agent Bakery know there's some plugins to ship
- Move `web/plugins/wato/keydb.py` to your Check_MK WATO directory: `/omd/sites/<SITE>/local/share/check_mk/web/plugins/wato/keydb.py`
    - This file will allow you to create a CheckMK Rule for this new plugin. Only agents matching a rule will have the plugin shipped to them.
- Move `agent_plugins/keydb` to your Check_MK plugin directory: `/omd/sites/<SITE>/local/lib/check_mk/base/plugins/agent_based/keydb`
    - This file will be baked into the agent by the bakery script
- Move `checks/keydb_servers.py` to your Check_MK checks directory: `/omd/sites/<SITE>/local/share/check_mk/agents/plugins/keydb_servers.py`
    - This file will be run on the server, parsing the sections from the agent

Now restart your CheckMK site.

## Configuration

Add a rule to your WATO configuration to enable the plugin for your KeyDB instances.
