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
