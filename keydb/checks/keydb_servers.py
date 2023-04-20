#!/usr/bin/env python3

from .agent_based_api.v1 import register, Service, Result, State, Metric

# <<<keydb_info>>>
# [[[MY_FIRST_REDIS|127.0.0.1|6380]]]
# ...

#   .--Server--------------------------------------------------------------.
#   |                   ____                                               |
#   |                  / ___|  ___ _ ____   _____ _ __                     |
#   |                  \___ \ / _ \ '__\ \ / / _ \ '__|                    |
#   |                   ___) |  __/ |   \ V /  __/ |                       |
#   |                  |____/ \___|_|    \_/ \___|_|                       |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'

# ...
# Server
# keydb_version:4.0.9
# keydb_git_sha1:00000000
# keydb_git_dirty:0
# keydb_build_id:9435c3c2879311f3
# keydb_mode:standalone
# os:Linux 4.15.0-1065-oem x86_64
# arch_bits:64
# multiplexing_api:epoll
# atomicvar_api:atomic-builtin
# gcc_version:7.4.0
# process_id:1029
# run_id:27bb4e37e85094b590b4693d6c6e11d07cd6400a
# tcp_port:6380
# uptime_in_seconds:29349
# uptime_in_days:0
# hz:10
# lru_clock:15193378
# executable:/usr/bin/keydb-server
# config_file:/etc/keydb/keydb2.conf
#
# Description of possible output:
# keydb_version: Version of the Redis server
# keydb_git_sha1: Git SHA1
# keydb_git_dirty: Git dirty flag
# keydb_build_id: The build id
# keydb_mode: The server's mode ("standalone", "sentinel" or "cluster")
# os: Operating system hosting the Redis server
# arch_bits: Architecture (32 or 64 bits)
# multiplexing_api: Event loop mechanism used by Redis
# atomicvar_api: Atomicvar API used by Redis
# gcc_version: Version of the GCC compiler used to compile the Redis server
# process_id: PID of the server process
# run_id: Random value identifying the Redis server (to be used by Sentinel and Cluster)
# tcp_port: TCP/IP listen port
# uptime_in_seconds: Number of seconds since Redis server start
# uptime_in_days: Same value expressed in days
# hz: The server's frequency setting
# lru_clock: Clock incrementing every minute, for LRU management
# executable: The path to the server's executable
# config_file: The path to the config file


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

    return name.replace(";", ":"), d


def discover_keydb_function(section):
    name, _ = parse_section(section)
    yield Service(item=name + " Server Info")
    yield Service(item=name + " Clients")
    yield Service(item=name + " Persistence")


def check_keydb_info(item, section):
    name, info = parse_section(section)

    if len(info) == 0:
        return

    if "Server Info" in item:
        yield from output_servers_info(info)
    elif "Clients" in item:
        yield from output_clients_info(info)
    elif "Persistence" in item:
        yield from output_persistence_info(info)
    else:
        yield Result(state=State.CRIT, summary=f"Unknown item: {item}")


def output_persistence_info(info):
    return
    yield


def output_clients_info(info):
    for data_key, param_key, infotext in [
        ("connected_clients", "connected", "Number of client connections"),
        ("client_longest_output_list", "output", "Longest output list"),
        ("client_biggest_input_buf", "input", "Biggest input buffer"),
        ("blocked_clients", "blocked", "Number of clients pending on a blocking call"),
    ]:
        clients_value = info.get(data_key)
        if clients_value is None:
            continue

        # upper_level = params.get("%s_upper" % param_key, (None, None))
        # lower_level = params.get("%s_lower" % param_key, (None, None))

        yield Metric(
            name="clients_%s" % param_key,
            value=int(clients_value),
            # TODO: boundaries from parameters
        )
        yield Result(
            state=State.OK,
            summary="%s: %s" % (infotext, clients_value),
        )

        # yield check_levels(
        #     clients_value,
        #     "clients_%s" % param_key,
        #     None,
        #     # upper_level + lower_level,
        #     human_readable_func=int,
        #     infoname=infotext,
        #     )


def output_servers_info(info):
    server_mode = info.get("keydb_mode")
    if server_mode is not None:
        mode_state = 0
        infotext = "Mode: %s" % server_mode.title()
        # TODO: Parse expected mode in parameters
        # mode_params = params.get("expected_mode")
        # if mode_params is not None:
        #     if mode_params != server_mode:
        #         mode_state = 1
        #         infotext += " (expected: %s)" % mode_params.title()

        yield mode_state, infotext

    # TODO: Parse server uptime
    server_uptime = info.get("uptime_in_seconds")
    if server_uptime is not None:
        yield Result(state=State.OK, summary=f"Uptime: {server_uptime} seconds")
    #     yield check_uptime_seconds(params, server_uptime)

    for key, infotext in [
        ("redis_version", "Version"),  # keydb_version does not exist
        ("gcc_version", "GCC compiler version"),
        ("process_id", "PID"),
    ]:
        value = info.get(key)
        if value is not None:
            yield Result(state=State.OK, summary=f"{key}: {value}")

    host_data = info.get("host")
    if host_data is not None:
        addr = "Socket" if info.get("port") == "unix-socket" else "IP"
        yield Result(state=State.OK, summary=f"${addr}: {host_data}")

    port_data = info.get("port")
    if port_data is not None and port_data != "unix-socket":
        yield Result(state=State.OK, summary=f"Port: {port_data}")


register.check_plugin(
    name="keydb_info",
    service_name="KeyDB %s",
    discovery_function=discover_keydb_function,
    check_function=check_keydb_info,
)
