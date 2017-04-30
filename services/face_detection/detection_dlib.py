import dlib

face_detector = dlib.get_frontal_face_detector()


def detect(image):
    im_height, im_width, _ = image.shape
    faces_array = face_detector(image, 1)

    faces = []
    for face in faces_array:
        x, y = max(face.left(), 0), max(face.top(), 0)
        w, h = min(face.right(), im_width) - x, min(face.bottom(), im_height) - y
        faces.append(dict(rect=list((x, y, w, h))))
    return faces
