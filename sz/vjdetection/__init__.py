import os
import cv2
import cv2.cv as cv
import numpy as np


def validate_shape(value):
    if not isinstance(value, np.ndarray):
        raise TypeError('image must be a ndarray')
    if value.ndim != 3:
        raise ValueError('image must have 3 axis')
    if value.shape[2] != 3:
        raise ValueError('image must have shape (width, height, 3)')
    return True


class ResizingFactor:

    def __init__(self, max_length):
        self.max_length = max_length

    def calc(self, image):
        validate_shape(image)
        length0, length1, color_depth = image.shape
        length = length1 and length1 > length0 or length0
        if length > self.max_length:
            return float(self.max_length) / float(length)
        else:
            return 1.0

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
        factor = ResizingFactor(self.__rate).calc(image)
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


def detect_object(uploaded_photo, cascade_path):
    array = bytearray(uploaded_photo.read())
    buffer = np.asarray(array, dtype=np.uint8)
    detector = ObjectDetector(cascade_path, min_size=0.01)
    # http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html
    circles = detector.detect(buffer)
    image = cv2.imdecode(buffer, flags=cv2.CV_LOAD_IMAGE_UNCHANGED)
    side1, side2, color_depth = image.shape
    size = side1
    if side2 > side1:
        size = side2
    if len(circles) > 0:
        for circle in circles:
            center = tuple([int(coord * size) for coord in circle[:2]])
            cv2.circle(image, center, int(circle[2] * size), (0, 0, 255))
    result, encoded_image = cv2.imencode('.jpg', image, None)
    if result:
        return encoded_image.data
    else:
        return None