"""Apply Motion Blur."""
from enum import Enum
import numpy as np
import cv2
from discolight.params.params import Params
from .augmentation.types import Augmentation, BoundedNumber
from .decorators.accepts_probs import accepts_probs


class Direction(Enum):

    """Corresponding enum objects for 8 directions."""

    DOWN = "DOWN"
    UP = "UP"
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    TOPRIGHT = "TOPRIGHT"
    TOPLEFT = "TOPLEFT"
    BOTTOMLEFT = "BOTTOMLEFT"
    BOTTOMRIGHT = "BOTTOMRIGHT"


@accepts_probs
class MotionBlur(Augmentation):

    """Add motionblur to a given image."""

    def __init__(self, kernel_size, direction):
        """Construct a MotionBlur augmenation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        super().__init__()

        self.kernel_size = kernel_size
        self.direction = direction

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add(
            "kernel_size",
            "Specify the kernel size, greater the size, the more the motion",
            BoundedNumber(int, minimum=0, maximum=None),
            10).add("direction",
                    "direction in which the blur is pointer towards",
                    Direction, 'DOWN')

    def augment(self, img, bboxes):
        """Augment an image."""
        kernel = np.zeros((self.kernel_size, self.kernel_size))

        if self.direction == Direction.DOWN:
            kernel[:, int(
                (self.kernel_size - 1) / 2)] = np.ones(self.kernel_size)
            kernel /= self.kernel_size
            new_img = cv2.filter2D(img, -1, kernel)
        elif self.direction == Direction.UP:
            img_rotate_180 = cv2.rotate(img, cv2.ROTATE_180)
            kernel[:, int(
                (self.kernel_size - 1) / 2)] = np.ones(self.kernel_size)
            kernel /= self.kernel_size
            up = cv2.filter2D(img_rotate_180, -1, kernel)
            new_img = cv2.rotate(up, cv2.ROTATE_180)
        elif self.direction == Direction.LEFT:
            kernel[int(
                (self.kernel_size - 1) / 2), :] = np.ones(self.kernel_size)
            kernel /= self.kernel_size
            new_img = cv2.filter2D(img, -1, kernel)
        elif self.direction == Direction.RIGHT:
            img_rotate_180 = cv2.rotate(img, cv2.ROTATE_180)
            kernel[int(
                (self.kernel_size - 1) / 2), :] = np.ones(self.kernel_size)
            kernel /= self.kernel_size
            right = cv2.filter2D(img_rotate_180, -1, kernel)
            new_img = cv2.rotate(right, cv2.ROTATE_180)
        elif self.direction == Direction.TOPLEFT:
            ind = np.diag_indices(self.kernel_size)
            kernel[ind] = np.ones(self.kernel_size)
            kernel /= self.kernel_size
            new_img = cv2.filter2D(img, -1, kernel)
        elif self.direction == Direction.BOTTOMRIGHT:
            img_rotate_90_clockwise = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            ind = np.diag_indices(self.kernel_size)
            kernel[ind] = np.ones(self.kernel_size)
            kernel = np.flip(kernel, axis=1)
            kernel /= self.kernel_size
            bottom_right = cv2.filter2D(img_rotate_90_clockwise, -1, kernel)
            new_img = cv2.rotate(bottom_right, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif self.direction == Direction.TOPRIGHT:
            img_rotate_90_clockwise = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            ind = np.diag_indices(self.kernel_size)
            kernel[ind] = np.ones(self.kernel_size)
            kernel /= self.kernel_size
            top_right = cv2.filter2D(img_rotate_90_clockwise, -1, kernel)
            new_img = cv2.rotate(top_right, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif self.direction == Direction.BOTTOMLEFT:
            ind = np.diag_indices(self.kernel_size)
            kernel[ind] = np.ones(self.kernel_size)
            kernel = np.flip(kernel, axis=1)
            kernel /= self.kernel_size
            new_img = cv2.filter2D(img, -1, kernel)

        return new_img, bboxes
