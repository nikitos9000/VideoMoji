NAME = 'capture'


def api(params):
    if params['source'] == 'webcam':
        import webcam
        scale = float(params['scale'])
        return webcam.capture(scale)

    if params['source'] == 'video':
        import sys
        import video
        scale = float(params['scale'])
        return video.capture(scale, sys.argv[1])

    if params['source'] == 'microphone':
        import microphone
        return microphone.capture(params['duration'])

    return
