import cv2
import openface

image_dim = 224
align = openface.AlignDlib('data/face_recognition/openface/shape_predictor_68_face_landmarks.dat')
net = openface.TorchNeuralNet('data/face_recognition/openface/VGG_FACE.t7', image_dim)


def recognize_faces(image, faces):
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    for face in faces:
        (x, y, w, h) = face['rect']
        face_img_rgb = img_rgb[y:y+h, x:x+w, :]

        face_bounding_box = align.getLargestFaceBoundingBox(face_img_rgb, skipMulti=True)
        face_aligned = align.align(image_dim, face_img_rgb, face_bounding_box,
                                   landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        features = net.forward(face_aligned)
        face['features'] = features.tolist()
    return face
