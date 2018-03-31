import cv2


def test_opencv_version():
    assert cv2.__version__ == '3.4.0'
