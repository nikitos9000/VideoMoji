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


def select_largest_face(faces):
    wh = 0
    largest_face = None
    for face in faces:
        x, y, w, h = face['rect']
        if w*h > wh:
            wh = w*h
            largest_face = face
    return largest_face


from collections import defaultdict
history = defaultdict(list)


def update_history(values):
    if values:
        result = {}
        for key, value in values.iteritems():
            history[key].append(value)
            key_history = history[key][-3:]
            result[key] = sum(key_history) / len(key_history)
        return result


def convert_emotions(emotions):
    emotions['angry'] *= 0.8
    emotions['fear'] *= 0.7
    emotions['happy'] *= 2.0
    emotions['surprise'] *= 2.0
    emotions['neutral'] *= 1.0
    emotions['sad'] *=0.25
    return emotions

idx = 0

@route('/api', method='POST')
def api():
    global idx
    response.content_type = 'application/json'
    image_base64 = request.forms['imgBase64']
    image_base64 = image_base64.replace('data:image/png;base64,', '')
    image = base64.urlsafe_b64decode(image_base64)

    idx += 1
    frame = dashboard.read_frame_from_string(image)
    frame, faces, voice = dashboard.media_process(idx, frame, [])
    face = select_largest_face(faces)

    image = dashboard.write_frame_to_string(frame)
    image_base64 = base64.b64encode(image)
    image_base64 = 'data:image/png;base64,' + image_base64

#    emotions = face and convert_emotions(face['emotions'])
    emotions = face and 'emotions' in face and face['emotions']

    metrics = {
        'engagement': 0.5,
        'goodwill': 0.8
    }

    emotions = update_history(emotions)

    return json.dumps({'imgBase64': image_base64, 'emotions': emotions, 'metrics': metrics})


@route('/<path:path>')
def static(path):
    return static_file(path, os.path.dirname(os.path.abspath(__file__)))


@route('/')
def root():
    return static('index.html')


if __name__ == '__main__':
#    dashboard.run_voice_thread()
    run(host='0.0.0.0', port=8080, server='gevent')
