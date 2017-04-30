#!/usr/bin/env python
import os
import sys
import json
import base64
from gevent import monkey; monkey.patch_all()
import bottle
bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024
from bottle import run, request, response, static_file, route

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dashboard


@route('/api', method='POST')
def api():
    import time
    s1 = time.time()
    response.content_type = 'application/json'
    image_base64 = request.forms['imgBase64']
    image_base64 = image_base64.replace('data:image/png;base64,', '')
    image = base64.urlsafe_b64decode(image_base64)

    frame = dashboard.read_frame_from_string(image)
    s2 = time.time()
    dashboard.media_process(frame, [])
    s3 = time.time()

    image = dashboard.write_frame_to_string(frame)
    image_base64 = base64.b64encode(image)
    image_base64 = 'data:image/png;base64,' + image_base64
    s4 = time.time()
    print 'STAT:', (s2-s1), (s3-s2), (s4-s3), 'total:', (s4-s1)

    return json.dumps({'imgBase64': image_base64})


@route('/<path:path>')
def static(path):
    return static_file(path, os.path.dirname(os.path.abspath(__file__)))


@route('/')
def root():
    return static('index.html')


if __name__ == '__main__':
#    dashboard.run_voice_thread()
    run(host='0.0.0.0', port=8080, server='gevent')
