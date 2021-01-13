#!/usr/bin/env python

# Copyright (c) 2020, MeteoSwiss
# Authors: Philipp Falke <philipp.falke@meteoswiss.ch>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
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
