import cv2

from keras.models import model_from_json


def _init_model():
    with open('data/face_emotions/keras/model.json') as model_file:
        model_json = model_file.read()
    model = model_from_json(model_json)
    model.load_weights('data/face_emotions/keras/model.h5')
    return model

emotions_model = _init_model()


def _predict_face_emotions(face):
    resized_img = cv2.resize(face, (48, 48), interpolation=cv2.INTER_AREA)
    image = resized_img.reshape(1, 1, 48, 48)
    list_of_list = emotions_model.predict(image, batch_size=1, verbose=1)
    angry, fear, happy, sad, surprise, neutral = [prob for lst in list_of_list for prob in lst]
    return dict(angry=angry, fear=fear, happy=happy, sad=sad, surprise=surprise, neutral=neutral)


def _predict_faces(frame, faces):
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, 1)
    for face in faces:
        (x, y, w, h) = face['rect']
        face_image_gray = img_gray[y:y+h, x:x+w]
        emotion_probs = _predict_face_emotions(face_image_gray)
        yield emotion_probs


def extract_emotions(frame, faces):
    face_with_emotions = []

    for face, face_emotions in zip(faces, _predict_faces(frame, faces)):
        face['emotions'] = face_emotions
        face_with_emotions.append(face)

    return face_with_emotions
