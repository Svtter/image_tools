import cv2


def gaussian(img, thresh: list):
    """
    Gaussian blur for image recognition.
    """

    res = []
    for i in thresh:
        res.append(cv2.GaussianBlur(img, (5, 5), 0))

    return res
