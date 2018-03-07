#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:3cx_sbc_connections",
    DropdownChoice(
        title = _("3CX SBC Connections (Linux)"),
        help = _("This will deploy the agent plugin <tt>ceph</tt> for monitoring the status of 3CX SBC Connections."),
        choices = [
            ( True, _("Deploy plugin for 3CX SBC Connections") ),
            ( None, _("Do not deploy plugin for 3CX SBC Connections") ),
        ]
    )
)

