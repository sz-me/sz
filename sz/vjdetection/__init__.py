import cv2
import cv2.cv as cv
import numpy as np
from sz.vjdetection import detectors


def detect_object(uploaded_photo, cascade_path):
    array = bytearray(uploaded_photo.read())
    buffer = np.asarray(array, dtype=np.uint8)
    detector = detectors.ObjectDetector(cascade_path, min_size=0.01)
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