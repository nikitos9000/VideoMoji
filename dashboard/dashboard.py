#!/usr/bin/env python

import os
import sys
import cv2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def request_capture_service():
    from services import capture
    return capture.api(dict(source='webcam', scale=0.5))


def request_face_detection_service(frame):
    from services import face_detection
    return face_detection.api(dict(image=frame, algo='opencv'))


def request_face_emotions_service(frame, faces):
    from services import face_emotions
    return face_emotions.api(dict(image=frame, faces=faces, algo='keras'))


def loop():
    frame = request_capture_service()
    faces = request_face_detection_service(frame)
    faces_with_emotions = request_face_emotions_service(frame, faces)
    print faces
    print faces_with_emotions
    return frame


if __name__ == '__main__':
    while True:
        cv2_frame = loop()
        cv2.imshow('Video', cv2_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
