from .. import utils

PORT = 8082
NAME = 'FaceEmotions'


@utils.timer
def api(params):
    if params['algo'] == 'keras':
        import emotions_keras
        return emotions_keras.extract_emotions(params['image'], params['faces'])

    if params['algo'] == 'ms':
        import emotions_ms
        return emotions_ms.extract_emotions(params['image'], params['faces'])
    return
