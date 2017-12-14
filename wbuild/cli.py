# -*- coding: utf-8 -*-
"""CLI interface to wbuild."""

import os
import click
import wbuild
import pathlib
import shutil
import distutils.dir_util


def setup_paths():
    """Setup the wbuild paths
    """
    templatePath = pathlib.Path(wbuild.__file__).parent / 'template'
    wbuildPath = pathlib.Path(wbuild.__file__).parent / '.wBuild'
    demoPath = pathlib.Path(wbuild.__file__).parent / 'demo'
    return templatePath, wbuildPath, demoPath


@click.group()
def main():
    # main command. We could also have some standard flags like --debug:
    #
    # @click.group()
    # @click.option('--debug/--no-debug', default=False)
    # def main(debug):
    #     click.echo('Debug mode is %s' % ('on' if debug else 'off'))
    pass


# --------------------------------------------
# commands

@main.command()
def init():
    """Initialize the repository with wbuild.

    This will create a .wBuild/ folder in the current path
    """
    # TODO - check if .git exists - warn if it doesn't
    templatePath, wbuildPath, demoPath = setup_paths()
    distutils.dir_util.copy_tree(str(wbuildPath), './.wBuild')
    click.echo("init...done")


# TODO - add the directory path as optional
@main.command()
def demo():
    """Setup a demo wBuild demo project
    """
    templatePath, wbuildPath, demoPath = setup_paths()
    shutil.copy(str(templatePath / 'Snakefile'), '.')
    shutil.copy(str(templatePath / 'make.config'), '.')
    shutil.copy(str(templatePath / 'readme.md'), '.')
    distutils.dir_util.copy_tree(str(wbuildPath), './.wBuild')
    distutils.dir_util.copy_tree(str(demoPath), '.')
    click.echo("demo...done")


@main.command()
def update():
    """Update the .wBuild folder to the most recent version of wBuild
    """
    # - check if .wBuild exists
    #   - if it doesn't, return the error
    # - if it does, update it
    if not os.path.exists(".wBuild"):
        raise ValueError(".wBuild doesn't exists. Please run wBuild init first or move to the right directory")

    click.echo("Removing .wBuild")
    shutil.rmtree(".wBuild")
    click.echo("Running .Init")
    init()
    click.echo("update...done")
