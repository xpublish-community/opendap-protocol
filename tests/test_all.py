import opendap_protocol as dap

import xdrlib
import numpy as np

XDRPACKER = xdrlib.Packer()

def test_dods_encode():

    XDRPACKER.reset()

    testdata = np.array(range(100), dtype=np.float32)

    XDRPACKER.pack_int(np.asarray(len(testdata)).astype('<i4'))
    XDRPACKER.pack_int(np.asarray(len(testdata)).astype('<i4'))
    XDRPACKER.pack_farray(len(testdata), testdata, XDRPACKER.pack_float)
    xdrpacked = XDRPACKER.get_buffer()

    assert xdrpacked == dap.dods_encode(testdata, dap.Float32)
