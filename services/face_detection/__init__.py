PORT = 8081
NAME = 'FaceDetection'


def api(params):
    if params['algo'] == 'opencv':
        import face_opencv
        return face_opencv.detect(params['image'])

    return
