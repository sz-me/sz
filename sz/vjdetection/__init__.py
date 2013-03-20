import os
import cv2
import cv2.cv as cv
import numpy as np


HAAR_CASCADES_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'vjdetection/data')


def get_haar_cascade_choices():
    files = os.listdir(HAAR_CASCADES_DIRECTORY)
    xmls = filter(lambda x: x.endswith('.xml'), files)
    return [(xml, xml) for xml in xmls]


def get_haar_cascade_path(haar_cascade_filename):
    return os.path.join(HAAR_CASCADES_DIRECTORY, haar_cascade_filename)


def detect_face(uploaded_photo, haar_cascade):
    array = bytearray(uploaded_photo.read())
    buffer = np.asarray(array, dtype=np.uint8)
    # http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html
    img = cv2.imdecode(buffer, flags=cv2.CV_LOAD_IMAGE_UNCHANGED)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    cascade = cv2.CascadeClassifier(haar_cascade)
    rectangles = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1, flags=cv.CV_HAAR_SCALE_IMAGE)
    if len(rectangles) > 0:
        rectangles[:,2:] += rectangles[:,:2]
        for x1, y1, x2, y2 in rectangles:
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, encoded_image = cv2.imencode('.jpg', img, encode_param)
    if result:
        return encoded_image.data
    else:
        return None