#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# @author Markus Plischke <m.plischke@q-mex.net>, Etienne Bruines <e.bruines@q-mex.net>
# @company Q-MEX Networks https://www.q-mex.net
# @source https://github.com/qmexnetworks/check_mk/blob/master/gude_pdu_phase/gude_pdu_phase.py

from .agent_based_api.v1 import *

# Get phase Values (Current) from GUDE PDU via SNMP


def discover_gude_pdu_phase(section):
    for line in section:
        yield Service(item=line[0])


def check_gude_pdu_phase(item, section):
    for name, value in section:
        if name == item:
            var = float(value) / 1000
            yield Metric(
                "A",
                var,
            )
            yield Result(
                state=State.OK,
                summary=f"Current: {var} A",
            )
            return

    yield Result(
        state=State.WARN,
        summary="Item %r not found in section" % item,
    )


register.snmp_section(
    name="gude_pdu_phase",
    detect=startswith(".1.3.6.1.2.1.1.0", "Expert Power Control"),  # sysDescr
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.28507.56.1.5.1.2.1",
        oids=[  # Current in ampere and the name (not necessarily in this order)
            "100",
            "5",
        ],
    ),
)

register.check_plugin(
    name="gude_pdu_phase",
    service_name="Current %s",
    discovery_function=discover_gude_pdu_phase,
    check_function=check_gude_pdu_phase,
)
