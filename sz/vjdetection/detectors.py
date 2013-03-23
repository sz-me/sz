import os
import cv2
import cv2.cv as cv
from sz.vjdetection import math


HAAR_CASCADES_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'vjdetection/data')


class CascadeFileManager:

    @classmethod
    def choices(cls):
        files = os.listdir(HAAR_CASCADES_DIRECTORY)
        xmls = sorted(filter(lambda x: x.endswith('.xml'), files))
        return [(xml, xml) for xml in xmls]

    @classmethod
    def path(cls, cascade_filename):
        return os.path.join(HAAR_CASCADES_DIRECTORY, cascade_filename)


class ObjectDetector:

    __rate = 512

    def __init__(self, cascade_filename, min_size=None, max_size=None):
        self.__cascade = cv2.CascadeClassifier(cascade_filename)
        if min_size is not None and max_size is not None:
            if min_size > max_size:
                raise ValueError('min_size must be less then max_size')
        self.__min_size = min_size
        self.__max_size = max_size

    def __normalize_image(self, image):
        factor = math.resizing_factor(image, self.__rate)
        resized = cv2.resize(image, (int(image.shape[1] * factor), int(image.shape[0] * factor)))
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        return gray

    def __n(self, value):
        return value / float(self.__rate)

    def __n_array(self, array):
        return [self.__n(el) for el in array]

    def __incircle(self, rectangle):
        x, y = rectangle[:2]
        dx, dy = rectangle[2:]
        x0 = x + 0.5 * dx
        y0 = y + 0.5 * dy
        r = 0.5 * (dx and (dx > dy) or dy)
        return [x0, y0, r]

    def detect(self, image_buf):
        image = cv2.imdecode(image_buf, flags=cv2.CV_LOAD_IMAGE_UNCHANGED)
        normalized_image = self.__normalize_image(image)
        kwargs = dict(flags=cv.CV_HAAR_SCALE_IMAGE)
        if self.__min_size is not None:
            kwargs['minSize'] = (int(self.__rate * self.__min_size), int(self.__rate * self.__min_size))
        if self.__max_size is not None:
            kwargs['maxSize'] = (int(self.__rate * self.__max_size), int(self.__rate * self.__max_size))
        rectangles = self.__cascade.detectMultiScale(normalized_image, **kwargs)
        if len(rectangles) > 0:
            circles = [self.__incircle(rectangle) for rectangle in rectangles]
            return [self.__n_array(circle) for circle in circles]
        else:
            return []


FACE_MIN_SIZE = 0.05


class FaceDetectorBase(ObjectDetector):

    def __init__(self, cascade_filename, min_size=FACE_MIN_SIZE):
        ObjectDetector.__init__(self, cascade_filename, min_size=min_size)


class FrontalFaceDetector(FaceDetectorBase):

    def __init__(self):
        cascade_filename = CascadeFileManager.path('haarcascade_frontalface_default.xml')
        FaceDetectorBase.__init__(cascade_filename)


class ProfileFaceDetector(FaceDetectorBase):

    def __init__(self):
        cascade_filename = CascadeFileManager.path('haarcascade_profileface.xml')
        FaceDetectorBase.__init__(cascade_filename)


class EyePairDetectorBase(ObjectDetector):

    def __init__(self, cascade_filename, min_size=FACE_MIN_SIZE / 2):
        ObjectDetector.__init__(self, cascade_filename, min_size=min_size)


class BigEyePairDetector(EyePairDetectorBase):

    def __init__(self):
        cascade_filename = CascadeFileManager.path('haarcascade_mcs_eyepair_big.xml')
        EyePairDetectorBase.__init__(self, cascade_filename)


class SmallEyePairDetector(EyePairDetectorBase):

    def __init__(self):
        cascade_filename = CascadeFileManager.path('haarcascade_mcs_eyepair_small.xml')
        EyePairDetectorBase.__init__(self, cascade_filename)
