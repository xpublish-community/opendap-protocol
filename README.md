opendap-protocol
================



[![Build Status](https://travis-ci.com/MeteoSwiss/opendap-protocol.svg?branch=master)](https://travis-ci.com/MeteoSwiss/opendap-protocol) [![codecov](https://codecov.io/gh/MeteoSwiss/opendap-protocol/branch/master/graph/badge.svg)](https://codecov.io/gh/MeteoSwiss/opendap-protocol) [![Documentation Status](https://readthedocs.org/projects/opendap-protocol/badge/?version=latest)](https://opendap-protocol.readthedocs.io/en/latest/?badge=latest) [![PyPI version](https://badge.fury.io/py/opendap-protocol.svg)](https://badge.fury.io/py/opendap-protocol)



A pure Python implementation of the OPeNDAP server protocol.

This module allows you to serve arbitrary data structures through the web
framework of your choice as OPeNDAP data objects. It implements just the bare
minimum of the DAP 2.0 protocol: DDS, DAS, and DODS responses and slicing. Array
data needs to be supplied as `numpy.ndarray` or as `dask.array.Array`.
