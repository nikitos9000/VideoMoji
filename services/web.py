#!/usr/bin/env python

import sys
import imp
import json
from gevent import monkey; monkey.patch_all()
from bottle import run, route, request, response


def load_module(name):
    return imp.load_source(name, name + '.py')


@route('/api', method='POST')
def api():
    params = request.forms
    result = module.api(params)
    response.add_header('Content-Type', 'application/json')
    return json.dumps(result)


if __name__ == '__main__':
    module = load_module(sys.argv[1])

    run(host='0.0.0.0', port=module.PORT, server='gevent')
