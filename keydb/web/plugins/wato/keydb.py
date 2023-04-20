#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cmk.gui.i18n import _
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
)
from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
from cmk.gui.valuespec import (
    Age,
    Dictionary,
    TextAscii,
)

def _valuespec_keydb():
    return Dictionary(
        title=_("KeyDB Status (Linux)"),
        help=_("This will deploy the KeyDB plugin."),
        elements=[],
        optional_keys=[],
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupMonitoringAgentsAgentPlugins,
        name="agent_config:keydb",
        valuespec=_valuespec_keydb,
    ))
