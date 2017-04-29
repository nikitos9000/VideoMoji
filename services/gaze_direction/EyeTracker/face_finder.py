import cv, cv2
import numpy


def pipeline_each(data, fns):
    return reduce(lambda a, x: map(x, a), fns, data)


class FaceFinder(object):
    def __init__(self, min_neighbors, min_eyeface_ratio, max_eyeface_ratio):
        self.max_eyeface_ratio = max_eyeface_ratio # detected eyes, at their biggest, seem to be no bigger than between 1/3 and 1/2 of the face in both dimensions (used to set a max eye size for the Haar classifier)
        self.min_eyeface_ratio = min_eyeface_ratio # detected eyes, at their biggest, seem to be no bigger than between 1/3 and 1/2 of the face in both dimensions (used to set a max eye size for the Haar classifier)
        self.min_neighbors = min_neighbors

        # for OpenCV face/eye classification methods:
        self.eye_cascade = cv2.CascadeClassifier('data/gaze_direction/haarcascade_eye.xml')

    @staticmethod
    def get_subimg(image, (x, y, w, h)):
        subimg = cv.CreateImage((w, h,), 8, 3)
        src_region = cv.GetSubRect(image, (x, y, w, h))
        cv.Copy(src_region, subimg)
        return subimg

    # TODO: write cv2 versions of this eventually:
    def find_eyes(self, image, f):
        (fx, fy, fw, fh) = f

        [max_width, max_height] = pipeline_each([fw, fh], [lambda x: x * self.max_eyeface_ratio, round, int])
        [min_width, min_height] = pipeline_each([fw, fh], [lambda x: x * self.min_eyeface_ratio, round, int])

        faceimg = self.get_subimg(image, f)

        # TODO : maybe figure this out later why these parameters help...
        eyes = self.eye_cascade.detectMultiScale(numpy.asarray(faceimg[:, :]), minNeighbors=self.min_neighbors)#, maxSize = max_eye)

        if eyes != ():
            # make their coordinates refer to the image frame and not the face box:
            eyes[:, 0] += f[0]
            eyes[:, 1] += f[1]

            # keep only "eyes" that are not too big or small (detectMultiScale() seems to do this somehow, but the documentation is insufficient)
            eyes = [e for e in eyes if e[2] < max_width and e[3] < max_height]
            eyes = [e for e in eyes if e[2] > min_width and e[3] > min_height]

        return eyes
