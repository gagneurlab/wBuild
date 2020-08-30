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
    print(help_result.output)
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


def test_wBuildDemo_dryRun(testdirectory):
    run_dir = testdirectory.mkdir("demo_test_dryrun")
    run_dir.run("wbuild demo")
    r = run_dir.run("snakemake -n")
    message = "This was a dry-run (flag -n). The order of jobs does not reflect the order of execution."
    assert message in r.stdout.output
    assert "\t18" in r.stdout.output


def test_wBuildDemo_isRun(testdirectory):
    run_dir = testdirectory.mkdir("demo_test_run")
    run_dir.run("wbuild demo")
    r = run_dir.run("snakemake --cores 1")
    assert "Finished job 0." in r.stderr.output
    assert "18 of 18 steps (100%) done" in r.stderr.output


def test_wBuildDemo_subindex(testdirectory):
    run_dir = testdirectory.mkdir("demo_test_subindex")
    run_dir.run("wbuild demo")
    r = run_dir.run("snakemake subIndex --cores 1")
    assert "Finished job 0." in r.stderr.output
    assert "3 of 3 steps (100%) done" in r.stderr.output

