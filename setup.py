#!/usr/bin/env python

# Copyright (C) 2018, MeteoSwiss, Philipp Meier <philipp.meier@meteoswiss.ch>

from setuptools import setup, find_packages


requirements = [
    'numpy',
]
setup_requirements = [
    'setuptools_scm',
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

extras = {
    'test': test_requirements,
}

packages = find_packages(include=['opendap_protocol'])

package_dir = {}

package_data = {}


setup(
    name='opendap-protocol',
    use_scm_version=True,
    author="Philipp Falke",
    author_email='philipp.falke@meteoswiss.ch',
    description='A pure Python implementation of the OPeNDAP server protocol.',
    url='https://github.com/MeteoSwiss/opendap-protocol',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD-3-Clause License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='opendap_protocol',
    entry_points={},
    scripts=[],
    license="BSD-3-Clause license",
    long_description=open('README.md').read() + '\n\n' +
                     open('HISTORY.rst').read(),
    include_package_data=True,
    zip_safe=False,
    test_suite='test',
    py_modules=['opendap-protocol'],
    packages=packages,
    install_requires=requirements,
    package_dir=package_dir,
    package_data=package_data,
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    extras_require=extras,
    )
