opendap_protocol
================

[![pipeline status](https://gitlab.meteoswiss.ch/APP/opendap-protocol/badges/master/pipeline.svg)](https://gitlab.meteoswiss.ch/APP/opendap-protocol/commits/master)
[![coverage report](https://gitlab.meteoswiss.ch/APP/opendap-protocol/badges/master/coverage.svg)](https://gitlab.meteoswiss.ch/APP/opendap-protocol/commits/master)



A pure Python implementation of the OPeNDAP server protocol.

This module allows you to serve arbitrary data structures through the web
framework of your choice as OPeNDAP data objects. It implements just the bare
minimum of the DAP 2.0 protocol: DDS, DAS, and DODS responses and slicing. Array
data needs to be supplied as `numpy.ndarray`.
