#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# @author Markus Plischke <m.plischke@q-mex.net>, Etienne Bruines <e.bruines@q-mex.net>
# @company Q-MEX Networks https://www.q-mex.net
# @source https://github.com/qmexnetworks/check_mk/blob/master/schleifenbauer_dpm3_phase/schleifenbauer_dpm3_phase.py

from .agent_based_api.v1 import *

# Get Values, Current etc. from Schleifenbauer DPM3 via SNMP


def discover_schleifenbauer_dpm3_phase(section):
    for line in section:
        yield Service(item=line[0])  # name


def check_schleifenbauer_dpm3_phase(item, section):
    for name, amp, volt, watt in section:
        if name == item:
            var_amp = float(amp) / 100
            var_volt = float(volt) / 100
            var_watt = float(watt)
            yield Metric(
                "A",
                var_amp,
            )
            yield Metric(
                "V",
                var_volt,
            )
            yield Metric(
                "W",
                var_watt,
            )
            yield Result(
                state=State.OK,
                summary=f"{var_amp} A, {var_volt} V, {var_watt} W",
            )
            return

    yield Result(
        state=State.WARN,
        summary="Item %r not found in section" % item,
    )

register.snmp_section(
    name="schleifenbauer_dpm3_phase",
    detect=startswith(".1.3.6.1.2.1.1.0", "Schleifenbauer"),  # sysDescr
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.31034.12.1.1.2.6.1.1",
        oids=[
            "1.1",  # Name
            "5.1",  # Current in ampere
            "7.1",  # Voltage in volt
            "9.1",  # Power in watt
        ],
    ),
)


register.check_plugin(
    name="schleifenbauer_dpm3_phase",
    service_name="Phase L%s",
    discovery_function=discover_schleifenbauer_dpm3_phase,
    check_function=check_schleifenbauer_dpm3_phase,
)
