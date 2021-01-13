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

from opendap_protocol.protocol import dods_encode
import opendap_protocol as dap

import xdrlib
import numpy as np
import dask.array as da
from functools import reduce

XDRPACKER = xdrlib.Packer()


def test_dods_encode():

    testdata = np.array(range(100), dtype=np.float32)

    xdrpacked = pack_xdr_float(testdata)

    assert xdrpacked == b''.join(dap.dods_encode(testdata, dap.Float32))

    assert b'\x00\x00\x00\x00' == b''.join(dap.dods_encode(0, dap.Float32))

    arrdata = np.asarray([1, 2, 3])
    assert b''.join(dap.dods_encode(
        arrdata, dap.Float64)) == pack_xdr_double_array(arrdata)

    # test dask vs numpy
    x_dim = 28
    y_dim = 30
    time_dim = 8
    vertical_dim = 1
    real_dim = 21
    ref_time_dim = 3

    np_data = np.arange(
        0, x_dim * y_dim * time_dim * vertical_dim * real_dim *
        ref_time_dim).reshape(
            (x_dim, y_dim, time_dim, vertical_dim, real_dim, ref_time_dim))

    data_vals = da.from_array(np_data,
                              chunks=(14, y_dim, 1, vertical_dim, 1, 1))

    x = dap.dods_encode(data_vals, dap.Int32)
    y = dap.dods_encode(np_data, dap.Int32)
    assert b''.join(x) == b''.join(y)

    int_arrdata = np.arange(0, 20, 2, dtype='<i4')
    assert b''.join(dods_encode(int_arrdata,
                                dap.Int32)) == pack_xdr_int_array(int_arrdata)


def test_parse_slice():

    assert dap.parse_slice(':') == Ellipsis
    assert dap.parse_slice('3:7') == slice(3, 8)
    assert dap.parse_slice('4') == 4


def test_parse_slice_constraint():

    assert dap.parse_slice_constraint('[0][:][:][4:7]') == (0, Ellipsis,
                                                            Ellipsis,
                                                            slice(4, 8))
    assert dap.parse_slice_constraint('[0][:][:]') == (0, Ellipsis, Ellipsis)
    assert dap.parse_slice_constraint('[0][:]') == (0, Ellipsis)
    assert dap.parse_slice_constraint('[0]') == (0, )
    assert dap.parse_slice_constraint('[]') == (Ellipsis, )


def test_meets_constraint():

    assert dap.meets_constraint('', 'test.object.path')

    assert dap.meets_constraint('test.object.path', 'test')
    assert dap.meets_constraint('test.object.path', 'test.object')
    assert dap.meets_constraint('test.object.path', 'test1.object') is False


def test_DAPObject():

    ob1 = dap.DAPObject(name='Object 1')
    assert ob1.name == 'Object_1'

    ob2 = dap.DAPObject(name='Object_2', parent=ob1)
    assert ob2.name == 'Object_2'
    assert ob2.parent.name == 'Object_1'

    ob3 = dap.DAPObject(name=1)
    assert ob3.name == 1


def test_Dataset():

    dataset = dap.Dataset(name='data')
    assert dataset.name == 'data'
    assert dataset.parent is None
    assert dataset.indent == ''
    assert dataset.data_path == ''

    assert b'Data:' in b''.join(dataset.dods_data())

    ob1 = dap.DAPObject(name='Object 1')

    dataset.append(ob1)

    assert ob1.data_path == 'Object_1'
    assert ob1.indent == '    '


def test_Attribute():

    dataset = dap.Dataset(name='test')

    attr1 = dap.Attribute(name='Attribute 1', value=3, dtype=dap.Float32)
    attr2 = dap.Attribute(name='Attribute 2',
                          value='a string',
                          dtype=dap.String)

    dataset.append(attr1, attr2)

    assert attr1.indent == '    '
    assert attr2.indent == '    '

    assert 'Float32' in ''.join(attr1.das())
    assert '"' in ''.join(attr2.das())

    assert 'Attribute' not in ''.join(dataset.dds())


def test_DAPAtom():
    pass


def test_complete_dap_response():

    expected_das = 'Attributes {\n'\
                   '    x {\n' \
                   '    }\n' \
                   '    y {\n' \
                   '    }\n'\
                   '    z {\n'\
                   '        String units "second";\n'\
                   '        Float64 size 4;\n'\
                   '    }\n'\
                   '}\n'

    expected_dds = 'Dataset {\n'\
                   '    Int16 x[x = 2];\n' \
                   '    Int16 y[y = 2];\n'\
                   '    Grid {\n'\
                   '      Array:\n'\
                   '        Int32 z[x = 2][y = 2];\n'\
                   '      Maps:\n' \
                   '        Int16 x[x = 2];\n' \
                   '        Int16 y[y = 2];\n'\
                   '    } z;\n'\
                   '} test;\n'

    expected_dods_data = b'\nData:\r\n\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x0a\x00\x00\x00\x0b\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x0a\x00\x00\x00\x0b'

    dataset = dap.Dataset(name='test')
    x = dap.Array(name='x', data=np.array([0, 1]), dtype=dap.Int16)
    y = dap.Array(name='y', data=np.array([10, 11]), dtype=dap.Int16)

    z = dap.Grid(name='z',
                 data=np.array([[0, 0], [0, 0]]),
                 dtype=dap.Int32,
                 dimensions=[x, y])

    z_attr = [
        dap.Attribute(name='units', value='second', dtype=dap.String),
        dap.Attribute(name='size', value=4, dtype=dap.Float64),
    ]
    z.append(*z_attr)

    dataset.append(x, y, z)

    assert ''.join(dataset.das()) == expected_das
    assert ''.join(dataset.dds()) == expected_dds
    assert b''.join(
        dataset.dods()) == expected_dds.encode() + expected_dods_data

    assert x.parent == dataset
    assert y.parent == dataset


def pack_xdr_float(data):
    XDRPACKER.reset()
    XDRPACKER.pack_int(np.asarray(len(data)).astype('<i4'))
    XDRPACKER.pack_int(np.asarray(len(data)).astype('<i4'))
    XDRPACKER.pack_farray(len(data), data, XDRPACKER.pack_float)
    return XDRPACKER.get_buffer()


def pack_xdr_double_array(data):
    XDRPACKER.reset()
    XDRPACKER.pack_int(np.asarray(len(data)))
    XDRPACKER.pack_int(np.asarray(len(data)))
    XDRPACKER.pack_farray(len(data), data.astype('<f8'), XDRPACKER.pack_double)
    return XDRPACKER.get_buffer()


def pack_xdr_int_array(data):
    XDRPACKER.reset()
    XDRPACKER.pack_int(np.asarray(len(data)))
    XDRPACKER.pack_int(np.asarray(len(data)))
    XDRPACKER.pack_farray(len(data), data.astype('<i4'), XDRPACKER.pack_int)
    return XDRPACKER.get_buffer()
