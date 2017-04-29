PORT = 8082
NAME = 'FaceEmotions'


def api(params):
    if params['algo'] == 'keras':
        import emotions_keras
        return emotions_keras.extract_emotions(params['image'], params['faces'])

    return
