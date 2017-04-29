import cv2

faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')


def detect(frame):
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY,1)

    faces = faceCascade.detectMultiScale(
        img_gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    return [dict(rect=list(face_rect)) for face_rect in faces]
