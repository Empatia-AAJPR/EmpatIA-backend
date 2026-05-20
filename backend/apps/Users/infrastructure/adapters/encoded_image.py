import cv2


def encode(img):
    if not img:
        return None

    img_array = cv2.imread(str(img))

    if img_array is None:
        return None

    ext = str(img).rpartition('.')[-1]

    _, img_encoded = cv2.imencode(f'.{ext}', img_array)

    return img_encoded