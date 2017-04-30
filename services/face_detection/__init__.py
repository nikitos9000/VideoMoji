from .. import utils

PORT = 8081
NAME = 'FaceDetection'


@utils.timer
def api(params):
    if params['algo'] == 'opencv':
        import detection_opencv
        return detection_opencv.detect(params['image'])

    if params['algo'] == 'dlib':
        import detection_dlib
        return detection_dlib.detect(params['image'])

    return
