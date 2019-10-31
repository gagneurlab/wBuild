#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 5):
    print("At least Python 3.5 is required.\n", file=sys.stderr)
    exit(1)

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'click-log',
    'PyYAML>=4.2b1',
    'snakemake>=5.5.1',
]

setup_requirements = [
    'pytest-runner',
    'pyyaml>=4.2b1'
    # TODO(wachutka): put setup requirements (distutils extensions, etc.) here
    # --- this todo really needed?
]

test_requirements = [
    'pytest',
    'pytest-testdirectory',
]

setup(
    name='wbuild',
    version='1.6.4',
    description="Automatic build tool for R Reports",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    author="Leonhard Wachutka",
    author_email='leonhard@wachutka.eu',
    url='https://github.com/gagneurlab/wBuild',
    packages=find_packages(include=['wbuild', 'pyyaml']),
    entry_points={
        'console_scripts': [
            'wbuild=wbuild.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='wbuild',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
