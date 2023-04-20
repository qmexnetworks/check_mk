#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from .bakery_api.v1 import (
    OS,
    DebStep,
    RpmStep,
    SolStep,
    Plugin,
    PluginConfig,
    SystemBinary,
    Scriptlet,
    WindowsConfigEntry,
    register,
    FileGenerator,
    ScriptletGenerator,
    WindowsConfigGenerator,
    quote_shell_string,
)
from pathlib import Path
from typing import TypedDict


def get_keydb_plugin_files(conf: dict) -> FileGenerator:
    yield Plugin(
        base_os=OS.LINUX,
        source=Path('keydb'),
        target=Path('keydb'),
        interval=60,  # one minute
    )

    # Do not yield PluginConfig, because we do not configure the plugin via CheckMK, but locally


class BakeryKeyDBConfig(TypedDict, total=False):
    # We do not need any configuration for this plugin - passwords etc. are defined locally on each machine
    # TODO: We may add config about warn/crit levels?
    pass


def get_keydb_scriptlets(conf: BakeryKeyDBConfig) -> ScriptletGenerator:
    installed_lines = ['logger -t Checkmk_Agent "Installed keydb"']
    uninstalled_lines = ['logger -t Checkmk_Agent "Uninstalled keydb"']

    yield Scriptlet(step=DebStep.POSTINST, lines=installed_lines)
    yield Scriptlet(step=DebStep.POSTRM, lines=uninstalled_lines)


# Register the bakery plugin
register.bakery_plugin(
    name="keydb",
    files_function=get_keydb_plugin_files,
    scriptlets_function=get_keydb_scriptlets,
)
