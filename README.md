opendap-protocol
================

A pure Python implementation of the OPeNDAP server protocol.

This module allows you to serve arbitrary data structures through the web
framework of your choice as OPeNDAP data objects. It implements just the bare
minimum of the DAP 2.0 protocol: DDS, DAS, and DODS responses and slicing. Array
data needs to be supplied as `numpy.ndarray`.
