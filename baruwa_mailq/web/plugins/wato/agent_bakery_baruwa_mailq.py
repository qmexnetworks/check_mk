#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:baruwa_mailq",
    DropdownChoice(
        title = _("Baruwa Mailq (Linux)"),
        help = _("This will deploy the agent plugin <tt>baruwa_mailq/tt> for monitoring the status of Baruwa Mail Queues"),
        choices = [
            ( True, _("Deploy plugin for Baruwa Mail Queues") ),
            ( None, _("Do not deploy plugin for Baruwa Mail Queues") ),
        ]
    )
)

# subgroup_networking =   _("Networking")

register_check_parameters(
        subgroup_applications,
        "baruwa_mailq",
        _("Baruwa Mail Queues"),
        Dictionary(
                help = _("This ruleset can be used to change the connection count warning and crit levels or to disable them."),
                elements = [
                        ("count",
                                Tuple(
                                        title = _("Number of Mails in Queue"),
                                        elements = [
                                                Integer(title = _("Warning at"), default_value = 0, min_value = 0 ),
                                                Integer(title = _("Critical at"), default_value = 0, min_value = 0 ),
                                                ],
                                        help = _("You can adjust the number of mails in queue before this service goes into warning/critical. Set to 0 to disable."),
                                        ),
                                ),
                        ],
                optional_keys = False,
        ),
        TextAscii(
                title = _("Baruwa Mail Queues"),
                help = _("Specify the amount of baruwa_mailq"),
                allow_empty = True
        ),
        'dict'
)

