#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wbuild` package."""

from click.testing import CliRunner
from wbuild import cli


def test_help():
    """Test the cli help functions"""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help' in help_result.output
    assert 'Show this message and exit.' in help_result.output


def test_init(testdirectory):
    """Test the cli help functions"""
    init_dir = testdirectory.mkdir("init")
    r = init_dir.run("wbuild init")
    assert r.stdout.match('*init...done*')


def test_demo(testdirectory):
    """Test the cli help functions"""
    init_dir = testdirectory.mkdir("demo")
    r = init_dir.run("wbuild demo")
    assert r.stdout.match('*demo...done*')

    r = init_dir.run("snakemake")
