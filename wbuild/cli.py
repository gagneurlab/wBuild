# -*- coding: utf-8 -*-
"""CLI interface to wbuild."""

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
    templatePath, wbuildPath, demoPath = setup_paths()
    distutils.dir_util.copy_tree(str(wbuildPath), './.wBuild')
    click.echo("Init...done")


@main.command()
def demo():
    templatePath, wbuildPath, demoPath = setup_paths()
    shutil.copy(str(templatePath / 'Snakefile'), '.')
    shutil.copy(str(templatePath / 'make.config'), '.')
    shutil.copy(str(templatePath / 'readme.md'), '.')
    distutils.dir_util.copy_tree(str(wbuildPath), './.wBuild')
    distutils.dir_util.copy_tree(str(demoPath), '.')
    click.echo("demo...done")
