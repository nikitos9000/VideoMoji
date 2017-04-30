from .. import utils

PORT = 8084
NAME = 'GazeDirection'


@utils.timer
def api(params):
    if params['algo'] == 'eye-tracker':
        import EyeTracker
        return EyeTracker.detect_gaze(params['image'], params['faces'])

    return
