from .. import utils

PORT = 8086
NAME = 'FaceRecognition'


@utils.timer
def api(params):
    if params['algo'] == 'openface':
        import recognition_openface
        return recognition_openface.recognize_faces(params['frame'], params['faces'])

    return
