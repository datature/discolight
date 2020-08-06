import pytest
import numpy as np

from discolight.annotations import (annotations_to_numpy_array)
from discolight.augmentations.coarsedropout import CoarseDropout


@pytest.mark.usefixtures("sample_image")
def test_coarsedropout(sample_image):

    img, annotations = sample_image

    bboxes = annotations_to_numpy_array(annotations)

    augmentation = CoarseDropout(0.1, 25)

    aug_img, aug_bboxes = augmentation.augment(img.copy(), bboxes.copy())

    assert np.allclose(
        expected_aug_img, aug_img
    ), "Performing augmentation does not yield expected image"
    assert np.array_equal(
        bboxes, aug_bboxes
    ), "Performing augmentation does not yield original augmentation"
