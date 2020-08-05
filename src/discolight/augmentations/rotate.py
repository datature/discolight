"""An augmentation to rotate an image."""
import numpy as np
import cv2
from discolight.params.params import Params
from .bbox_utilities import bbox_utilities
from .augmentation.types import Augmentation
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class Rotate(Augmentation):

    """Rotate the given image."""

    def __init__(self, angle):
        """Construct a Rotate augmentation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        super().__init__()

        # cv2 rotates clockwise when angle is negative
        self.angle = -1 * angle

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("angle", "", float, 5)

    def augment(self, img, bboxes):
        """Augment an image."""
        angle = self.angle
        height, width = img.shape[0], img.shape[1]
        center_x, center_y = width // 2, height // 2
        transformation_matrix = cv2.getRotationMatrix2D(center=(center_x,
                                                                center_y),
                                                        angle=angle,
                                                        scale=1.0)
        sin_theta = np.abs(transformation_matrix[0][1])
        cos_theta = np.abs(transformation_matrix[0][0])
        new_width = int((width * cos_theta) + (height * sin_theta))
        new_height = int((width * sin_theta) + (height * cos_theta))
        translate_x = (new_width / 2) - center_x
        translate_y = (new_height / 2) - center_y
        transformation_matrix[0][2] = transformation_matrix[0][2] + translate_x
        transformation_matrix[1][2] = transformation_matrix[1][2] + translate_y
        rotated_img = cv2.warpAffine(img, transformation_matrix,
                                     (new_width, new_height))
        rotated_img_resized = cv2.resize(rotated_img, (width, height))
        # handle grayscale images with one channel, because cv2 will mess up
        # your  shape if your image is (28,28,1) it becomes (28,28)
        if len(rotated_img_resized.shape) == 2:
            rotated_img_resized = rotated_img_resized.reshape(height, width, 1)
            # code below transform the bboxes accordingly.
        corners = bbox_utilities.get_corners(bboxes)
        corners = np.hstack((corners, bboxes[:, 4:]))
        corners[:, :8] = bbox_utilities.rotate_box(corners[:, :8], angle,
                                                   center_x, center_y, height,
                                                   width)
        new_bbox = bbox_utilities.get_enclosing_box(corners)
        scale_factor_x = rotated_img.shape[1] / width
        scale_factor_y = rotated_img.shape[0] / height
        new_bbox[:, :4] = new_bbox[:, :4] / [
            scale_factor_x,
            scale_factor_y,
            scale_factor_x,
            scale_factor_y,
        ]
        bboxes = new_bbox
        bboxes = bbox_utilities.clip_box(bboxes, [0, 0, width, height], 0.25)
        return rotated_img_resized, bboxes
