#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wbuild` package."""

from click.testing import CliRunner
from wbuild import cli


def test_cli_help():
    """Test the cli help functions"""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help' in help_result.output
    assert 'Show this message and exit.' in help_result.output

# TODO - run the init
#
# TODO - run the demo
