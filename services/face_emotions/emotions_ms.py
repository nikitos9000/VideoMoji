import cv2
import cognitive_face

MS_COGNITIVE_FACE_API_KEY = '1fe40415d3d54b5d8072003afd8bc233'

MS_EMOTION_MIN_THR = 0.3
MS_SMILE_MIN_THR = 0.7
MS_STUBBLE_MIN_THR = 0.2
MS_STUBBLE_MAX_THR = 0.5
MS_BEARD_MIN_THR = 0.5
MS_MOUSTACHE_MIN_THR = 0.5

cognitive_face.Key.set(MS_COGNITIVE_FACE_API_KEY)


def _parse_faces_data(faces, faces_to_persons_ids):
    faces_data = []
    for face in faces:
        face_id = face['faceId']
        face_attributes = face['faceAttributes']

        age = int(face_attributes['age'])
        gender = face_attributes['gender']

        emotion, emotion_score = max(face_attributes['emotion'].iteritems(), key=lambda (_, score): score)
        emotion = emotion if emotion_score >= MS_EMOTION_MIN_THR else 'neutral'
        emotions = face_attributes['emotion']
        smile = face_attributes['smile'] >= MS_SMILE_MIN_THR
        stubble = MS_STUBBLE_MIN_THR <= face_attributes['facialHair']['sideburns'] < MS_STUBBLE_MAX_THR
        beard = face_attributes['facialHair']['beard'] >= MS_BEARD_MIN_THR
        moustache = face_attributes['facialHair']['moustache'] >= MS_MOUSTACHE_MIN_THR
        glasses = face_attributes['glasses'].lower()

        faces_data.append(dict(face_id=face_id, person_id=faces_to_persons_ids.get(face_id), age=age, gender=gender,
                               emotion=emotion, emotions=emotions, smile=smile, glasses=glasses, stubble=stubble, beard=beard,
                               moustache=moustache))
    return faces_data


def _detect_faces(image_url):
    face_attributes = ['age', 'gender', 'smile', 'facialHair', 'glasses', 'emotion']

    faces = cognitive_face.face.detect(image_url, face_id=True, landmarks=True, attributes=','.join(face_attributes))
    return faces


def extract_emotions(frame, faces):
    from StringIO import StringIO
    content = cv2.imencode('.jpg', frame)[1].tostring()

    faces_data = _parse_faces_data(_detect_faces(StringIO(content)), {})

    for face, data in zip(faces, faces_data):
        face['emotions'] = data['emotions']
    return faces
