import cv2

video_capture = cv2.VideoCapture(0)


def capture(scale):
    _, frame = video_capture.read()
    return cv2.resize(frame, None, fx=scale, fy=scale)
