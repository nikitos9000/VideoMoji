#!/usr/bin/env python

import os
import sys
import cv2
import time
import threading
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def request_video_capture_service():
    from services import capture
    return capture.api(dict(source='video', scale=1.0))


def request_face_detection_service(frame):
    from services import face_detection
#    import services
#    return services.api_call(dict(image=frame, algo='dlib'), face_detection.PORT)
    return face_detection.api(dict(image=frame, algo='dlib'))


def request_face_emotions_service(idx, frame, faces):
    from services import face_emotions

    if idx % 4 == 0:
        return face_emotions.api(dict(image=frame, faces=faces, algo='ms'))
    return faces


def request_gaze_direction_service(frame, faces):
    from services import gaze_direction
    return gaze_direction.api(dict(image=frame, faces=faces, algo='eye-tracker'))


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
        queue_audio_frames.extend(audio['samples'])
        queue_audio_sample_rate = audio['sample_rate']


def video_loop():
    video_frame = request_video_capture_service()
    media_process(0, video_frame, queue_audio_frames)
    del queue_audio_frames[:]

    return video_frame


def read_frame_from_string(frame_string):
    img_array = np.asarray(bytearray(frame_string), dtype=np.uint8)
    return cv2.imdecode(img_array, 3)


def write_frame_to_string(frame):
    content = cv2.imencode('.png', frame)[1]
    return content


def draw_face_frames(frame, faces):
    for face in faces:
        rect = face['rect']
        x, y, w, h = rect

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return frame


def draw_eye_frames(frame, faces):
    for face in faces:
        if 'eyes' in face:
            eyes = face['eyes']
            left_eye, right_eye = eyes
            left_pupil, left_eye_loc = left_eye
            right_pupil, right_eye_loc = right_eye
            left_x, left_y, left_w, left_h = left_eye_loc
            right_x, right_y, right_w, right_h = right_eye_loc

            cv2.rectangle(frame, (left_x, left_y), (left_x + left_w, left_y + left_h), (0, 0, 255), 2)
            cv2.rectangle(frame, (right_x, right_y), (right_x + right_w, right_y + right_h), (0, 0, 255), 2)

    return frame


def media_process(idx, video_frame, audio_samples):
    video_frame = request_video_capture_service()
    video_frame = cv2.resize(video_frame, None, fx=0.5, fy=0.5)
    faces = request_face_detection_service(video_frame)
    faces = request_face_emotions_service(idx, video_frame, faces)
    faces = request_gaze_direction_service(video_frame, faces)

    voice = request_audio_emotions_service(audio_samples)

    video_frame = draw_face_frames(video_frame, faces)
    video_frame = draw_eye_frames(video_frame, faces)

    print 'Faces:', faces
    print 'Voice:', voice

    return video_frame, faces, voice


def run_voice_thread():
    audio_thread = threading.Thread(target=audio_loop)
    audio_thread.daemon = True
    audio_thread.start()


if __name__ == '__main__':
    run_voice_thread()

    while True:
        start_time = time.time()
        cv2_frame = video_loop()
        cv2.imshow('Video', cv2_frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
