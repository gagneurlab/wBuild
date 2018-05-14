#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wbuild` command-line interface."""
from unittest import mock

import os
from click.testing import CliRunner
from wbuild import cli


def test_wBuildHelp_isShown():
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help' in help_result.output
    assert 'Show this message and exit.' in help_result.output


def test_newDirSuccessfullyInitiated(testdirectory):
    init_dir = testdirectory.mkdir("init")
    # create readme.md to avoid readme copying dialog
    open(init_dir.path() + '/readme.md', 'w+')
    r = init_dir.run("wbuild init")

    assert r.stdout.match('*init...done*')


def test_wBuildDemo_isCreated(testdirectory):
    init_dir = testdirectory.mkdir("demo_test")
    print("Directory created!")
    r = init_dir.run("wbuild demo")
    assert r.stdout.match('*demo...done*')

