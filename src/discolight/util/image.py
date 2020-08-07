"""Image loading and saving utilities."""
import numpy as np
import cv2

from discolight.annotations import annotations_to_numpy_array
from discolight.augmentations.bbox_utilities.bbox_utilities import draw_rect


def load_image_from_bytes(image_bytes):
    """Construct an OpenCV image from a byte array for augmenting.

    The image will be loaded in HxWxC format in RGB colorspace
    """
    np_bytes = np.array(bytearray(image_bytes))

    image = cv2.imdecode(np_bytes, cv2.IMREAD_COLOR)

    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def load_image(image_path):
    """Load an image from a file and prepares it for augmentation.

    The image will be loaded in HxWxC format in RGB colorspace.
    """
    with open(image_path, "rb") as image_file:
        return load_image_from_bytes(image_file.read())


def save_image(path, image, annotations=None, color=(255, 0, 0), stroke=8.0):
    """Save an image loaded with load_image or load_image_from_bytes.

    Keyword Arguments:
    path - The filename to save the image to. This must include an extension
           to indicate the format (e.g., .jpg, .png)
    image - The OpenCV image to save. This should have been originally
            loaded with load_image or load_image_from_bytes and optionally
            augmented
    annotations - An array of BoundingBox objects that will be drawn on top
                  of the image in red, or None if no annotations are to be
                  drawn.
    """
    img_copy = image.copy()

    if annotations is not None:

        bboxes = annotations_to_numpy_array(annotations)
        img_copy = draw_rect(img_copy, bboxes, color, stroke)

    img_copy = cv2.cvtColor(img_copy, cv2.COLOR_RGB2BGR)

    return cv2.imwrite(path, img_copy)
