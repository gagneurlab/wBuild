#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wbuild` command-line interface."""
from unittest import mock

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

    assert r.stderr.match('*init...done*')


def test_wBuildDemo_isCreated(testdirectory):
    demo_dir = testdirectory.mkdir("demo_test")
    print("Directory created!")
    r = demo_dir.run("wbuild demo")
    assert r.stderr.match('*demo...done*')


def test_wBuildDemo_isRun(testdirectory):
    run_dir = testdirectory.mkdir("demo_test_run")
    run_dir.run("wbuild demo")
    r = run_dir.run("snakemake -n")
    assert len(r.stdout.output) == 160

    run_dir.run("snakemake --cores 1")
    r = run_dir.run("snakemake -n")
    assert r.stdout.match("*Nothing to be done.*")


