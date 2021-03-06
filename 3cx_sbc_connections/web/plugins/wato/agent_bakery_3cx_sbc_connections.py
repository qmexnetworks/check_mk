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

# subgroup_networking =   _("Networking")

register_check_parameters(
        subgroup_applications,
        "3cx_sbc_connections",
        _("3CX SBC Connections"),
        Dictionary(
                help = _("This ruleset can be used to change the connection count warning and crit levels or to disable them."),
                elements = [
                        ("count",
                                Tuple(
                                        title = _("Number of Connections"),
                                        elements = [
                                                Integer(title = _("Warning at"), default_value = 0, min_value = 0 ),
                                                Integer(title = _("Critical at"), default_value = 0, min_value = 0 ),
                                                ],
                                        help = _("You can adjust the number of connections before this service goes into warning/critical. Set to 0 to disable."),
                                        ),
                                ),
                        ],
                optional_keys = False,
        ),
        TextAscii(
                title = _("SBC Connections"),
                help = _("Specify the amount of 3cx-sbc-connection"),
                allow_empty = True
        ),
        'dict'
)

