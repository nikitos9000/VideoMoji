import dlib

face_detector = dlib.get_frontal_face_detector()


def detect(image):
    faces_array = face_detector(image, 1)

    faces = []
    for face in faces_array:
        x, y = face.left(), face.top()
        w, h = face.right() - x, face.bottom() - y
        faces.append(dict(rect=list((x, y, w, h))))
    return faces
