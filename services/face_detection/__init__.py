PORT = 8081
NAME = 'FaceDetection'


def api(params):
    if params['algo'] == 'opencv':
        import detection_opencv
        return detection_opencv.detect(params['image'])

    return
