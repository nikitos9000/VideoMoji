from .. import utils

PORT = 8083
NAME = 'VoiceEmotions'


@utils.timer
def api(params):
    if params['algo'] == 'vokaturi':
        import emotions_vokaturi
        return emotions_vokaturi.extract_emotions(params['samples'], params['sample_rate'])

    return
