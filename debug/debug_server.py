# Copyright (c) 2018, MeteoSwiss,
# Author: Philipp Meier <philipp.meier@meteoswiss.ch>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
DAP debug server
================

A simple flask web service application for debugging the protocol.
"""

import logging

logging.basicConfig(level=logging.DEBUG)

import urllib
import numpy as np

from flask import Flask, Response, jsonify, request

import opendap_protocol as dap

app = Flask(__name__)


class BaseDataset(object):
    def dds(self, constraint=''):
        return self.dataset.dds(constraint=constraint)

    def das(self, constraint=''):
        return self.dataset.das(constraint=constraint)

    def dods(self, constraint=''):
        return self.dataset.dods(constraint=constraint)

    @classmethod
    def subclasses(cls):
        return dict([(sc.__name__, sc) for sc in cls.__subclasses__()])


class Test2DGrid(BaseDataset):
    @property
    def dataset(self):
        dataset = dap.Dataset(name='test')

        x = dap.Array(name='x', data=np.array([0, 1]), dtype=dap.Int16)
        y = dap.Array(name='y', data=np.array([10, 11]), dtype=dap.Int16)

        p = dap.Grid(
            name='p',
            data=np.array([[0, 0], [0, 0]]),
            dtype=dap.Int32,
            dimensions=[x, y])

        p_attr = [
            dap.Attribute(name='units', value='second', dtype=dap.String),
            dap.Attribute(name='size', value=4, dtype=dap.Float64),
        ]
        p.append(*p_attr)

        dataset.append(x, y, p)

        return dataset

    def _dods(self, constraint=''):
        if constraint == 'x,y,p.p':
            logging.debug(
                '2D Grid: Returning fake DODS response (which is known to work).'
            )

            return b'Dataset {\n    Int16 x[x = 2];\n    Int16 y[y = 2];\n    Grid {\n      Array:\n        Int32 p[x = 2][y = 2];\n      Maps:\n        Int16 x[x = 2];\n        Int16 y[y = 2];\n    } p;\n} test;\n\nData:\r\n\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\n\x00\x00\x00\x0b\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\n\x00\x00\x00\x0b'
        else:
            logging.debug('2D Grid: Returning normal response.')
            return self.dataset.dods(constraint=constraint)


class Test3DGrid(BaseDataset):
    @property
    def dataset(self):
        dataset = dap.Dataset(name='test')

        x = dap.Array(name='x', data=np.array([0, 1]), dtype=dap.Int16)
        y = dap.Array(name='y', data=np.array([10, 11]), dtype=dap.Int16)
        z = dap.Array(name='z', data=np.array([20, 21]), dtype=dap.Int16)

        p = dap.Grid(
            name='p',
            data=np.array([[[0, 0], [0, 0]], [[1, 1], [1, 1]]]),
            dtype=dap.Int32,
            dimensions=[x, y, z])

        p_attr = [
            dap.Attribute(name='units', value='second', dtype=dap.String),
            dap.Attribute(name='size', value=8, dtype=dap.Float64),
        ]
        p.append(*p_attr)

        dataset.append(x, y, z, p)

        return dataset


@app.route('/', methods=['GET'])
def index():
    return jsonify([k for k, v in BaseDataset.subclasses().items()])


@app.route('/<testcase>.dds', methods=['GET'])
def dds(testcase):
    constraint = urllib.parse.urlsplit(request.url)[3]
    return Response(
        BaseDataset.subclasses()[testcase]().dds(constraint=constraint),
        mimetype='text/plain')


@app.route('/<testcase>.das')
def das(testcase):
    constraint = urllib.parse.urlsplit(request.url)[3]
    return Response(
        BaseDataset.subclasses()[testcase]().das(constraint=constraint),
        mimetype='text/plain')


@app.route('/<testcase>.dods')
def dods(testcase):
    constraint = urllib.parse.urlsplit(request.url)[3]
    return Response(
        BaseDataset.subclasses()[testcase]().dods(constraint=constraint),
        mimetype='application/octet-stream')


if __name__ == '__main__':
    app.run(port=32111, debug=True)
