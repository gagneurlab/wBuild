# -*- coding: utf-8 -*-

"""Console script for wbuild."""

import click
import wbuild
import pathlib
import shutil
import distutils.dir_util


# TODO - this should be split into multiple sub-commands,
# leveraging the functionality of click
@click.command()
@click.argument('command')
def main(command):
    """Console script for wbuild."""

    # print(wbuild.__file__)
    templatePath = pathlib.Path(wbuild.__file__).parent / 'template'
    wbuildPath = pathlib.Path(wbuild.__file__).parent / '.wBuild'
    demoPath = pathlib.Path(wbuild.__file__).parent / 'demo'

    if command == 'init':
        distutils.dir_util.copy_tree(str(wbuildPath), './.wBuild')
        click.echo("Init...done")

    if command == 'demo':
        shutil.copy(str(templatePath / 'Snakefile'), '.')
        shutil.copy(str(templatePath / 'make.config'), '.')
        shutil.copy(str(templatePath / 'readme.md'), '.')
        distutils.dir_util.copy_tree(str(wbuildPath), './.wBuild')
        distutils.dir_util.copy_tree(str(demoPath), '.')
        click.echo("demo...done")


if __name__ == "__main__":
    main()
