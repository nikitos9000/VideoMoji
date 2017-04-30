#!/usr/bin/env python
import bottle
import json
import base64
import StringIO
from gevent import monkey; monkey.patch_all()
bottle.debug(True)
bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024
from bottle import run, request, response, static_file, route


@route('/api', method='POST')
def api():
    response.content_type = 'application/json'
    image_base64 = request.forms['imgBase64']
    image_base64 = image_base64.replace('data:image/png;base64,', '')
    image = base64.urlsafe_b64decode(image_base64)

    return json.dumps({})


@route('/<path:path>')
def static(path):
    return static_file(path, './')


@route('/')
def root():
    return static_file('index.html', './')


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, server='gevent')
