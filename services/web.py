#!/usr/bin/env python

import sys
import imp
import cPickle
from gevent import monkey; monkey.patch_all()
from bottle import run, route, request


def load_module(name):
    return imp.load_source(name, name + '/__init__.py')


@route('/api', method='POST')
def api():
    params = request.body.read()
    params = cPickle.loads(params)
    result = module.api(params)
    result = cPickle.dumps(result, protocol=2)
    return result


if __name__ == '__main__':
    module = load_module(sys.argv[1])

    run(host='0.0.0.0', port=module.PORT, server='gevent')
