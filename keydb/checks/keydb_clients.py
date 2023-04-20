#!/usr/bin/env python3

from .agent_based_api.v1 import register, Service, Result, State, Metric


# .
#   .--Clients-------------------------------------------------------------.
#   |                     ____ _ _            _                            |
#   |                    / ___| (_) ___ _ __ | |_ ___                      |
#   |                   | |   | | |/ _ \ '_ \| __/ __|                     |
#   |                   | |___| | |  __/ | | | |_\__ \                     |
#   |                    \____|_|_|\___|_| |_|\__|___/                     |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'

# ...
# Clients
# connected_clients:1
# client_longest_output_list:0
# client_biggest_input_buf:0
# blocked_clients:0

# Description of possible output:
# connected_clients - Number of client connections (excluding connections from replicas)
# client_longest_output_list - longest output list among current client connections
# client_biggest_input_buf - biggest input buffer among current client connections
# blocked_clients - Number of clients pending on a blocking call (BLPOP, BRPOP, BRPOPLPUSH)


def parse_section(section):
    d = dict()
    header = section[0][0]
    # Extract name from header
    # Extract `0.0.0.0;6379` from [[[0.0.0.0;6379|0.0.0.0|6379]]]
    name = header.split("[[[")[1].split("|")[0]

    for line in section[1:]:
        # line is a list of fields

        # Possibly starts with a #-Symbol comment
        if line[0].startswith("#"):
            continue

        if len(line) <= 1:
            continue

        key, value = line
        # Remove leading and trailing whitespace
        key = key.strip()
        value = value.strip()
        # Add to dictionary
        d[key] = value

    return name, d


def discover_keydb_function(section):
    name, _ = parse_section(section)
    yield Service(item=name)


def check_keydb_info_clients(item, section):
    _, clients_data = parse_section(section)

    created_some = False
    for data_key, param_key, infotext in [
        ("connected_clients", "connected", "Number of client connections"),
        ("client_longest_output_list", "output", "Longest output list"),
        ("client_biggest_input_buf", "input", "Biggest input buffer"),
        ("blocked_clients", "blocked", "Number of clients pending on a blocking call"),
    ]:
        clients_value = clients_data.get(data_key)
        if clients_value is None:
            continue

        # upper_level = params.get("%s_upper" % param_key, (None, None))
        # lower_level = params.get("%s_lower" % param_key, (None, None))

        yield Metric(
            name="clients_%s" % param_key,
            value=int(clients_value),
            # TODO: boundaries from parameters
        )
        created_some = True

        # yield check_levels(
        #     clients_value,
        #     "clients_%s" % param_key,
        #     None,
        #     # upper_level + lower_level,
        #     human_readable_func=int,
        #     infoname=infotext,
        #     )

    if created_some:
        yield Result(state=State.OK)


register.check_plugin(
    name="keydb_info_clients",
    service_name="KeyDB %s Clients",
    discovery_function=discover_keydb_function,
    check_function=check_keydb_info_clients,
)
