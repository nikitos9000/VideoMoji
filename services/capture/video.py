import cv2

video_capture = None


def capture(scale, filename):
    global video_capture
    if not video_capture:
        video_capture = cv2.VideoCapture(filename)

    _, frame = video_capture.read()
    return cv2.resize(frame, None, fx=scale, fy=scale)
