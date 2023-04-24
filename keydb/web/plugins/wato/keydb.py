#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cmk.gui.i18n import _
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
)
from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
from cmk.gui.valuespec import Age, Dictionary, DropdownChoice, MonitoringState, Integer, TextInput, Tuple


def _valuespec_keydb():
    return Dictionary(
        title=_("KeyDB Status (Linux)"),
        help=_("This will deploy the KeyDB plugin."),
        elements=[
            (
                "expected_mode",
                DropdownChoice(
                    title=_("Expected mode"),
                    choices=[
                        ("standalone", _("Standalone")),
                        ("sentinel", _("Sentinel")),
                        ("cluster", _("Cluster")),
                    ],
                ),
            ),
            (
                "min",
                Tuple(
                    title=_("Minimum required uptime"),
                    elements=[
                        Age(title=_("Warning if below")),
                        Age(title=_("Critical if below")),
                    ],
                ),
            ),
            (
                "max",
                Tuple(
                    title=_("Maximum allowed uptime"),
                    elements=[
                        Age(title=_("Warning at")),
                        Age(title=_("Critical at")),
                    ],
                ),
            ),
            (
                "connected_lower",
                Tuple(
                    title=_("Total number of client connections lower level"),
                    elements=[
                        Integer(
                            title=_("Warning below"),
                            unit="connections",
                        ),
                        Integer(
                            title=_("Critical below"),
                            unit="connections",
                        ),
                    ],
                ),
            ),
            (
                "connected_upper",
                Tuple(
                    title=_("Total number of client connections upper level"),
                    elements=[
                        Integer(
                            title=_("Warning at"),
                            unit="connections",
                        ),
                        Integer(
                            title=_("Critical at"),
                            unit="connections",
                        ),
                    ],
                ),
            ),
            (
                "output_lower",
                Tuple(
                    title=_("Longest output list lower level"),
                    elements=[
                        Integer(title=_("Warning below")),
                        Integer(title=_("Critical below")),
                    ],
                ),
            ),
            (
                "output_upper",
                Tuple(
                    title=_("Longest output list upper level"),
                    elements=[
                        Integer(title=_("Warning at")),
                        Integer(title=_("Critical at")),
                    ],
                ),
            ),
            (
                "input_lower",
                Tuple(
                    title=_("Biggest input buffer lower level"),
                    elements=[
                        Integer(title=_("Warning below"), unit="issues"),
                        Integer(title=_("Critical below"), unit="íssues"),
                    ],
                ),
            ),
            (
                "input_upper",
                Tuple(
                    title=_("Biggest input buffer upper level"),
                    elements=[
                        Integer(title=_("Warning at")),
                        Integer(title=_("Critical at")),
                    ],
                ),
            ),
            (
                "blocked_lower",
                Tuple(
                    title=_("Total number of clients pending on a blocking call lower level"),
                    elements=[
                        Integer(
                            title=_("Warning below"),
                            unit="clients",
                        ),
                        Integer(
                            title=_("Critical below"),
                            unit="clients",
                        ),
                    ],
                ),
            ),
            (
                "blocked_upper",
                Tuple(
                    title=_("Total number of clients pending on a blocking call upper level"),
                    elements=[
                        Integer(
                            title=_("Warning at"),
                            unit="clients",
                        ),
                        Integer(
                            title=_("Critical at"),
                            unit="clients",
                        ),
                    ],
                ),
            ),
            (
                "rdb_last_bgsave_state",
                MonitoringState(
                    title=_("State when last RDB save operation was faulty"), default_value=1
                ),
            ),
            (
                "aof_last_rewrite_state",
                MonitoringState(
                    title=_("State when Last AOF rewrite operation was faulty"), default_value=1
                ),
            ),
            (
                "rdb_changes_count",
                Tuple(
                    title=_("Number of changes since last dump"),
                    elements=[
                        Integer(title=_("Warning at"), unit="changes"),
                        Integer(title=_("Critical at"), unit="changes"),
                    ],
                ),
            ),
        ],
        optional_keys=[],
    )


rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupMonitoringAgentsAgentPlugins,
        name="agent_config:keydb",
        valuespec=_valuespec_keydb,
    ))
