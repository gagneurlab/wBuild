#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'click-log',
    'PyYAML>=3.12',
    'snakemake>=3.13.2',
    # TODO: put package requirements here
]

setup_requirements = [
    'pytest-runner',
    'pyyaml'
    # TODO(wachutka): put setup requirements (distutils extensions, etc.) here
    # --- this todo really needed?
]

test_requirements = [
    'pytest',
    'pytest-testdirectory',
]

setup(
    name='wbuild',
    version='1.2.0',
    description="Automatic build tool for R Reports",
    long_description=readme + '\n\n' + history,
    author="Leonhard Wachutka",
    author_email='leonhard@wachutka.eu',
    url='https://i12g-gagneurweb.in.tum.de/gitlab/wachutka/wBuild',
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
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
