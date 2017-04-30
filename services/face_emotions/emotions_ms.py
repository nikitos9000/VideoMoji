import cv2
import cognitive_face

MS_COGNITIVE_FACE_API_KEY = 'b545b42aab9b4bbcb7031a36fa25f8f6' #'1fe40415d3d54b5d8072003afd8bc233'

MS_EMOTION_MIN_THR = 0.3
MS_SMILE_MIN_THR = 0.7
MS_STUBBLE_MIN_THR = 0.2
MS_STUBBLE_MAX_THR = 0.5
MS_BEARD_MIN_THR = 0.5
MS_MOUSTACHE_MIN_THR = 0.5

cognitive_face.Key.set(MS_COGNITIVE_FACE_API_KEY)


def _parse_faces_data(faces):
    faces_data = []
    for face in faces:
        face_attributes = face['faceAttributes']

        emotion, emotion_score = max(face_attributes['emotion'].iteritems(), key=lambda (_, score): score)
        emotion = emotion if emotion_score >= MS_EMOTION_MIN_THR else 'neutral'
        emotions = face_attributes['emotion']

        faces_data.append(dict(emotion=emotion, emotions=emotions))
    return faces_data


def _detect_faces(image_url):
    face_attributes = ['emotion']

    faces = cognitive_face.face.detect(image_url, attributes=','.join(face_attributes))
    return faces


def extract_emotions(frame, faces):
    from StringIO import StringIO
    content = cv2.imencode('.jpg', frame)[1].tostring()

    faces_data = _parse_faces_data(_detect_faces(StringIO(content)))

    for face, data in zip(faces, faces_data):
        face['emotions'] = data['emotions']
    return faces
