# -*- coding: utf-8 -*-
"""CLI interface to wbuild."""

import os
import click
import wbuild
import pathlib
import shutil
import distutils.dir_util
import click_log
import logging
logger = logging.getLogger(__name__)
click_log.basic_config(logger)


def setup_paths():
    """Setup the wbuild paths
    """
    templatePath = pathlib.Path(wbuild.__file__).parent / 'template'
    wbuildPath = pathlib.Path(wbuild.__file__).parent / '.wBuild'
    demoPath = pathlib.Path(wbuild.__file__).parent / 'demo'
    return templatePath, wbuildPath, demoPath


@click.group()
@click_log.simple_verbosity_option(logger)
def main():
    pass


# --------------------------------------------
# commands

@main.command()
def init():
    """Initialize the repository with wbuild.

    This will create a .wBuild/ folder in the current path
    """
    # TODO - check if .git exists - warn if it doesn't
    if not os.path.exists(".git"):
        logger.warn("Not in a .git repository")
    if os.path.exists(".wBuild"):
        logger.error("ERROR: .wBuild already exists")
        # TODO exit
    templatePath, wbuildPath, demoPath = setup_paths()
    distutils.dir_util.copy_tree(str(wbuildPath), './.wBuild')
    logger.info("init...done")


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
    logger.info("demo...done")


@main.command()
def update():
    """Update the .wBuild folder to the most recent version of wBuild
    """
    # - check if .wBuild exists
    #   - if it doesn't, return the error
    # - if it does, update it
    if not os.path.exists(".wBuild"):
        raise ValueError(".wBuild doesn't exists. Please run wBuild init first or move to the right directory")

    logger.info("Removing .wBuild")
    shutil.rmtree(".wBuild")
    logger.info("Running .Init")
    templatePath, wbuildPath, demoPath = setup_paths()
    distutils.dir_util.copy_tree(str(wbuildPath), './.wBuild')
    logger.info("update...done")
