NAME = 'capture'


def api(params):
    scale = float(params['scale'])

    if params['source'] == 'webcam':
        import webcam
        return webcam.capture(scale)

    return
