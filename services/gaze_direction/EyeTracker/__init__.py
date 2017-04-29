import glob
import cv
from tree_ensemble import *
from face_finder import *

min_neighbors = 3
min_eyeface_ratio = 1.0/6.0
max_eyeface_ratio = 5.0/12.0
subsample = 1.0
exportgv = False
saveXML = False

ff = FaceFinder(min_neighbors, min_eyeface_ratio, max_eyeface_ratio)
tree_ens = TreeEnsemble(subsample, exportgv, saveXML)

tree_param_filelist = glob.glob('data/gaze_direction/random_forest_params/depth10ntrees100nimages14060/*.xml')
tree_ens.loadparams(tree_param_filelist)


def detect_gaze(image, faces):
    image = cv.fromarray(image)

    for face in faces:
        rect = face['rect']
        eyes_loc = ff.find_eyes(image, rect)

        num_eyes_found = numpy.shape(eyes_loc)[0]
        if num_eyes_found > 0:
            eyes_imgs = [numpy.asarray(ff.get_subimg(image, e)[:, :]) for e in eyes_loc]

            if len(eyes_imgs) == 2:
                left_pupil = tree_ens.predict_forest(eyes_imgs[0])
                right_pupil = tree_ens.predict_forest(eyes_imgs[1])

                left_eye = (left_pupil, eyes_loc[0])
                right_eye = (right_pupil, eyes_loc[1])
                face['eyes'] = (left_eye, right_eye)
    return faces
