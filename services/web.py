#!/usr/bin/env python

import sys
import imp
import json
import cPickle
from gevent import monkey; monkey.patch_all()
from bottle import run, route, request, response


def load_module(name):
    return imp.load_source(name, name + '/__init__.py')


@route('/api', method='POST')
def api():
#    params = json.loads(request.body.read().strip())
    params = request.body.read()
    params = cPickle.loads(params)
    result = module.api(params)
#    response.add_header('Content-Type', 'application/json')
#    response.
    result = cPickle.dumps(result)
    return result #json.dumps(result)


if __name__ == '__main__':
    module = load_module(sys.argv[1])

    run(host='0.0.0.0', port=module.PORT, server='gevent')
