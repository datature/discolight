"""An augmentation that randomly crops an image."""
import random
import cv2
import numpy as np
from discolight.params.params import Params
from .augmentation.types import Augmentation, BoundedNumber
from .decorators.accepts_probs import accepts_probs


def get_bboxes_in_cropped_area(x, y, w, h, bboxlist):
    """Filter out bounding boxes within the given cropped area."""
    bboxes = []

    for item in bboxlist:
        # if xmin is greater or equal to x, if bbox is inside the crop
        if ((item[0] >= x) and (item[1] >= y) and (item[2] <= (x + w))
                and (item[3] <= (y + h))):
            bboxes.append(item)
        else:
            continue

    return bboxes


@accepts_probs
class RandomCrop(Augmentation):

    """Randomly crops the given image."""

    def __init__(self, max_width, max_height):
        """Construct a RandomCrop augmenation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        self.max_width = max_width
        self.max_height = max_height

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("max_width",
                            "Maximum width of cropped area (normalized)",
                            BoundedNumber(float, 0, 1), 0.7).add(
                                "max_height",
                                "Maximum height of cropped area (normalized)",
                                BoundedNumber(float, 0, 1), 0.7)

    def augment(self, img, bboxes, iteration=100):
        """Augment an image."""
        if iteration <= 0:
            raise RuntimeError(
                "Couldn't find crop that did not keep some bounding boxes.")

        height, width, _ = img.shape

        crop_width = random.randint(0, int(width * self.max_width))
        crop_height = random.randint(0, int(height * self.max_height))

        x = random.randint(0, crop_width)
        y = random.randint(0, crop_height)
        reduced_bboxes = np.array(
            get_bboxes_in_cropped_area(x, y, crop_width, crop_height, bboxes))

        # if no bbox, get_aug return false; and recall .get_aug
        if len(reduced_bboxes) == 0 and len(bboxes) > 0:
            return self.augment(img, bboxes, iteration - 1)

        cropped_img = img[y:y + crop_height, x:x + crop_width]

        # u need the ratio for bounding boxes and images.
        width_ratio_resize = width / cropped_img.shape[1]
        height_ratio_resize = img.shape[0] / cropped_img.shape[0]
        resized_cropped_img = cv2.resize(cropped_img, (width, height))

        reduced_bboxes[:,
                       [0]] = (reduced_bboxes[:, [0]] - x) * width_ratio_resize
        reduced_bboxes[:,
                       [2]] = (reduced_bboxes[:, [2]] - x) * width_ratio_resize
        reduced_bboxes[:, [1]] = (reduced_bboxes[:, [1]] -
                                  y) * height_ratio_resize
        reduced_bboxes[:, [3]] = (reduced_bboxes[:, [3]] -
                                  y) * height_ratio_resize

        return resized_cropped_img, reduced_bboxes
