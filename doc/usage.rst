=====
Usage
=====

For more information on the DAP 2.0 protocol, visit
`the specification page <https://earthdata.nasa.gov/esdis/eso/standards-and-references/data-access-protocol-2>`_.

Create a DDS, DAS and DODS responses from arbitrary `numpy` arrays
-------------------------------------------------------------------

Basic imports::

    import numpy as np
    import opendap_protocol as dap


Define dimensions::

    x = dap.Array(name='x', data=np.array([0, 1, 2]), dtype=dap.Int16)
    y = dap.Array(name='y', data=np.array([10, 11, 12]), dtype=dap.Int16)
    z = dap.Array(name='z', data=np.array([20, 21, 22]), dtype=dap.Int16)


Define an array holding our data::

    data_array = dap.Grid(name='data',
                          data=np.random.rand(3, 3, 3),
                          dtype=dap.Float64,
                          dimensions=[x, y, z])


Define attributes::

    attrs = [
        dap.Attribute(name='units', value='m s-1', dtype=dap.String),
        dap.Attribute(name='version', value=2, dtype=dap.Int16),
    ]

and attach them to the data array::

    data_array.append(*attrs)

Glue it all together by creating the `Dataset` and appending to it::

    dataset = dap.Dataset(name='Example')
    dataset.append(x, y, z, data_array)

Each of the DAP 2.0 responses returns a `generator iterator`. Such a generator
has generally a low memory footprint, since the serialized data set does not
need to be held in memory at once. Rather, serialization takes place as a
consumer iterates through the data set.

For testing purposes, each response can be printed as string::

    print(''.join(dataset.dds()))

    # Dataset {
    # Int16 x[x = 3];
    # Int16 y[y = 3];
    # Int16 z[z = 3];
    # Grid {
    #   Array:
    #     Float64 data[x = 3][y = 3][z = 3];
    #   Maps:
    #     Int16 x[x = 3];
    #     Int16 y[y = 3];
    #     Int16 z[z = 3];
    #   } data;
    # } Example;

    print(''.join(dataset.das()))

    # Attributes {
    #     x {
    #     }
    #     y {
    #     }
    #     z {
    #     }
    #     data {
    #         String units "m s-1";
    #         Int16 version 2;
    #     }
    # }

    print(b''.join(dataset.dods()))

    # See for yourself ;-)

Serving data through a web service using Flask
----------------------------------------------

.. note::
    We assume, that the ``dataset`` created above is still available as a variable.

Basic setup::

    import urllib
    from flask import Flask, Response, request

    app = Flask(__name__)

Define the web service endpoints needed by the DAP protocol::

    @app.route('/dataset.dds', methods=['GET'])
    def dds_response():
        # Retrieve constraints from the request to handle slicing, etc.
        constraint = urllib.parse.urlsplit(request.url)[3]
        return Response(
            dataset.dds(constraint=constraint),
            mimetype='text/plain')

    @app.route('/dataset.das', methods=['GET'])
    def das_response():
        constraint = urllib.parse.urlsplit(request.url)[3]
        return Response(
            dataset.das(constraint=constraint),
            mimetype='text/plain')

    @app.route('/dataset.dods', methods=['GET'])
    def dods_response():
        constraint = urllib.parse.urlsplit(request.url)[3]
        return Response(
            dataset.dods(constraint=constraint),
            mimetype='application/octet-stream')

    app.run(debug=True)


Data can then be loaded from any Python terminal using ``xarray`` or
``netCDF4``.

.. note::
    Please be aware, that for opening a dataset the suffix (``.dds``, ``.das``
    or ``.dods``) needs to be omitted. The netCDF library figures out on its own
    which endpoint it has to call in what order.


``xarray``::

    import xarray as xr

    data = import xr.open_dataset('http://localhost:5000/dataset')
    data.load()

    # <xarray.Dataset>
    # Dimensions:  (x: 3, y: 3, z: 3)
    # Coordinates:
    #   * x        (x) int16 0 1 2
    #   * y        (y) int16 10 11 12
    #   * z        (z) int16 20 21 22
    # Data variables:
    #     data     (x, y, z) float64 0.7793 0.3464 0.1331 ... 0.2244 0.4277 0.1545


``netCDF4``::

    import netCDF4 as nc

    data = nc.Dataset('http://localhost:5000/dataset')
    data

    # <class 'netCDF4._netCDF4.Dataset'>
    # root group (NETCDF3_CLASSIC data model, file format DAP2):
    #     dimensions(sizes): x(3), y(3), z(3)
    #     variables(dimensions): int16 x(x), int16 y(y), int16 z(z), float64 data(x,y,z)
    #     groups:
