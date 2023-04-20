#!/usr/bin/env python3

from cmk.base.check_api import (
    check_levels,
    discover,
    get_age_human_readable,
    get_parsed_item_data,
    get_timestamp_human_readable,
)
from cmk.base.check_legacy_includes.uptime import check_uptime_seconds
from cmk.base.config import check_info, factory_settings

from .agent_based_api.v1 import register, Service, Result, State, Metric

# <<<keydb_info>>>
# [[[MY_FIRST_REDIS|127.0.0.1|6380]]]
# ...

# .
#   .--Persistence---------------------------------------------------------.
#   |           ____               _     _                                 |
#   |          |  _ \ ___ _ __ ___(_)___| |_ ___ _ __   ___ ___            |
#   |          | |_) / _ \ '__/ __| / __| __/ _ \ '_ \ / __/ _ \           |
#   |          |  __/  __/ |  \__ \ \__ \ ||  __/ | | | (_|  __/           |
#   |          |_|   \___|_|  |___/_|___/\__\___|_| |_|\___\___|           |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'

# ...
# Persistence
# loading:0
# rdb_changes_since_last_save:0
# rdb_bgsave_in_progress:0
# rdb_last_save_time:1578466632
# rdb_last_bgsave_status:ok
# rdb_last_bgsave_time_sec:-1
# rdb_current_bgsave_time_sec:-1
# rdb_last_cow_size:0
# aof_enabled:0
# aof_rewrite_in_progress:0
# aof_rewrite_scheduled:0
# aof_last_rewrite_time_sec:-1
# aof_current_rewrite_time_sec:-1
# aof_last_bgrewrite_status:ok
# aof_last_write_status:ok
# aof_last_cow_size:0

# Description of possible output:
# loading - Flag indicating if the load of a dump file is on-going
# rdb_changes_since_last_save - Number of changes since the last dump
# rdb_bgsave_in_progress - Flag indicating a RDB save is on-going
# rdb_last_save_time - Epoch-based timestamp of last successful RDB save
# rdb_last_bgsave_status - Status of last RDB save operation
# rdb_last_bgsave_time_sec - Duration of the last RDB save operation in seconds
# rdb_current_bgsave_time_sec - Duration of the on-going RDB save operation if any
# rdb_last_cow_size - size in bytes of copy-on-write allocations during last RDB save operation
# aof_enabled - Flag indicating AOF logging is activated
# aof_rewrite_in_progress - Flag indicating a AOF rewrite operation is on-going
# aof_rewrite_scheduled - Flag indicating an AOF rewrite operation will be scheduled once the on-going RDB save is complete.
# aof_last_rewrite_time_sec - Duration of last AOF rewrite operation in seconds
# aof_current_rewrite_time_sec - Duration of the on-going AOF rewrite operation if any
# aof_last_bgrewrite_status - Status of last AOF rewrite operation
# aof_last_write_status - Status of the last write operation to the AOF
# aof_last_cow_size - The size in bytes of copy-on-write allocations during the last AOF rewrite operation

factory_settings["keydb_info_persistence_default_levels"] = {
    "rdb_last_bgsave": 1,
    "aof_last_rewrite": 1,
}


def check_keydb_info_persistence(item, params, item_data):
    persistence_data = item_data.get(item, {}).get("Persistence")
    if not persistence_data or persistence_data is None:
        return

    for status, duration, infotext in [
        ("rdb_last_bgsave_status", "rdb_last_bgsave", "Last RDB save operation: "),
        ("aof_last_bgrewrite_status", "aof_last_rewrite", "Last AOF rewrite operation: "),
    ]:
        value = persistence_data.get(status)
        if value is not None:
            state = 0
            if value != "ok":
                state = params.get("%s_state" % duration)
                infotext += "faulty"
            else:
                infotext += "successful"

            duration_val = persistence_data.get("%s_time_sec" % duration)
            if duration_val is not None and duration_val != -1:
                infotext += " (Duration: %s)" % get_age_human_readable(duration_val)
            yield state, infotext

    rdb_save_time = persistence_data.get("rdb_last_save_time")
    if rdb_save_time is not None:
        yield 0, "Last successful RDB save: %s" % get_timestamp_human_readable(rdb_save_time)

    rdb_changes = persistence_data.get("rdb_changes_since_last_save")
    if rdb_changes is not None:
        yield check_levels(
            rdb_changes,
            "changes_sld",
            params.get("rdb_changes_count"),
            human_readable_func=int,
            infoname="Number of changes since last dump",
        )


register.check_plugin(
    # TODO: "default_levels_variable": "keydb_info_persistence_default_levels", ?
    name="keydb_info_persistence",
    service_name="KeyDB %s Persistence",
    discovery_function=discover(lambda k, values: "Persistence" in values),
    check_function=check_keydb_info_persistence,
)

