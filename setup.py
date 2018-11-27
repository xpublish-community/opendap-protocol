#!/usr/bin/env python

# Copyright (C) 2018, MeteoSwiss, Philipp Meier <philipp.meier@meteoswiss.ch>

from setuptools import setup, find_packages

import versioneer

setup(
    name='opendap-protocol',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Philipp Meier',
    author_email='philipp.meier@meteoswiss.ch',
    description='A pure Python implementation of the OPeNDAP server protocol.',
    packages=find_packages(),
    entry_points={},
    py_modules=['opendap_protocol'],
    include_package_data=True,
    license='MIT License',
    long_description=open('README.md').read(),
    install_requires=[
        'numpy',
    ])
