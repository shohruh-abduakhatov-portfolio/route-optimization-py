#!/usr/local/bin/python3.6

import json

from quart import Quart, request

from data import Data
from pdp import main

app = Quart(__name__)


@app.route('/optimize_route', methods=['GET'])
async def pdp_long():
    data = json.loads(request.args.get('data'))
    print("in >> ", data)
    _data = Data()
    _data.serialize(value=data)
    response = {}
    try:
        response = await main(_data)
    except Exception as e:
        print(e)
    print('[***] sending...')
    return json.dumps(response)


@app.route('/test')
async def hello():
    return 'mest'


app.run(port=5001)
