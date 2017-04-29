#!/usr/bin/env python

import os
import sys
import cv2
import time
import threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def request_video_capture_service():
    from services import capture
    return capture.api(dict(source='webcam', scale=0.5))


def request_face_detection_service(frame):
    from services import face_detection
    return face_detection.api(dict(image=frame, algo='opencv'))


def request_face_emotions_service(frame, faces):
    from services import face_emotions
    return face_emotions.api(dict(image=frame, faces=faces, algo='keras'))


def request_audio_capture_service():
    from services import capture
    return capture.api(dict(source='microphone', duration=5.0))


def request_audio_emotions_service(audio_frames):
    from services import voice_emotions
    result = voice_emotions.api(dict(algo='vokaturi', samples=audio_frames, sample_rate=queue_audio_sample_rate))
    return result


queue_audio_frames = []
queue_audio_sample_rate = 0


def audio_loop():
    global queue_audio_sample_rate
    while True:
        audio = request_audio_capture_service()
        queue_audio_frames.append(audio['samples'])
        queue_audio_sample_rate = audio['sample_rate']


def video_loop():
    video_frame = request_video_capture_service()
    faces = request_face_detection_service(video_frame)
    faces_with_emotions = request_face_emotions_service(video_frame, faces)
    voice_with_emotions = request_audio_emotions_service(queue_audio_frames)
    del queue_audio_frames[:]

    print 'Faces:', faces
    print 'Face Emotions:', faces_with_emotions
    print 'Voice Emotions:', voice_with_emotions
    return video_frame


if __name__ == '__main__':
    audio_thread = threading.Thread(target=audio_loop)
    audio_thread.daemon = True
    audio_thread.start()

    while True:
        start_time = time.time()
        cv2_frame = video_loop()
        cv2.imshow('Video', cv2_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        end_time = time.time()
        if end_time - start_time < 1.0/25:
            time.sleep(1.0/25 - (end_time - start_time))

    cv2.destroyAllWindows()
