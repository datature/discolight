import pytest
import numpy as np

from discolight.annotations import (annotations_to_numpy_array)
from discolight.augmentations.motionblur import MotionBlur, Direction


@pytest.mark.usefixtures("sample_image")
@pytest.mark.parametrize("direction", [
    Direction.UP, Direction.DOWN, Direction.RIGHT, Direction.LEFT,
    Direction.TOPRIGHT, Direction.TOPLEFT, Direction.BOTTOMRIGHT,
    Direction.BOTTOMLEFT
])
def test_motionblur(sample_image, direction):

    img, annotations = sample_image

    bboxes = annotations_to_numpy_array(annotations)

    augmentation = MotionBlur(kernel_size=10, direction=direction)

    aug_img, aug_bboxes = augmentation.augment(img.copy(), bboxes.copy())

    assert np.array_equal(bboxes, aug_bboxes)
    assert np.array_equal(img.shape, aug_img.shape)
