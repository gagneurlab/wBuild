# -*- coding: utf-8 -*-
"""CLI interface to wbuild."""

import sys
import os
import click
import wbuild
import pathlib
import shutil
import distutils.dir_util
import click_log
import logging
import wbuild.utils as utils
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
@click.version_option('1.6.0',prog_name='wBuild')
def main():
    pass


# --------------------------------------------
# commands

@main.command()
def init():
    """Initialize the repository with wbuild.

    This will prepare wBuild in the current project
    """
    if os.path.exists(".wBuild"):
        logger.error("ERROR: .wBuild already exists. Use update if you want to update the version")
        sys.exit(2)
    templatePath, wbuildPath, demoPath = setup_paths()
    distutils.dir_util.copy_tree(str(wbuildPath), './.wBuild')
    if not os.path.isfile("Snakefile"):
        shutil.copy(str(templatePath / 'Snakefile'), '.')
    if not os.path.isfile("wbuild.yaml"):
        shutil.copy(str(templatePath / 'wbuild.yaml'), '.')
    
    ### search for a file containing the word readme and .md
    readme_exists = False
    onlyfiles = [f for f in os.listdir(".") if os.path.isfile(os.path.join(".", f))]
    for f in onlyfiles:
        if ("readme" in f) and f.endswith(".md"):
            readme_exists = True
    if not readme_exists:
        copyReadme = input("wBuild needs readme.md in a root folder of your project. Shall we create the default "
                           "one? (y/n)")
        if 'y' in copyReadme:
            shutil.copy(str(templatePath / 'readme.md'), '.')
    utils.writeWbuildVersion()

    logger.info("init...done")


@main.command()
def demo():
    """Setup a demo wBuild demo project
    """
    if os.path.exists(".wBuild"):
        logger.error("ERROR: .wBuild already exists. Run demo in empty folder.")
        sys.exit(2)
    templatePath, wbuildPath, demoPath = setup_paths()
    shutil.copy(str(templatePath / 'Snakefile'), '.')
    shutil.copy(str(templatePath / 'wbuild.yaml'), '.')
    distutils.dir_util.copy_tree(str(wbuildPath), './.wBuild')
    distutils.dir_util.copy_tree(str(demoPath), '.')
    utils.writeWbuildVersion()
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
    shutil.rmtree("./.wBuild")
    # import subprocess
    # deprecatedPackages = subprocess.check_output(['pip','list','--outdated']).decode("utf-8")
    # if 'wbuild' in deprecatedPackages:
    #     logger.warning("Newer version of wBuild available.")
    #     updateConf = input("Update wBuild using pip (requires internet connection)? (y/n)")
    #     if 'y' in updateConf:
    #         subprocess.call(['pip','install','wbuild','--upgrade'])
    #         logger.info("wBuild successfully updated!")
    logger.info("Running .init")
    templatePath, wbuildPath, demoPath = setup_paths()
    distutils.dir_util.copy_tree(str(wbuildPath), './.wBuild')
    utils.writeWbuildVersion()
    logger.info("update...done")
