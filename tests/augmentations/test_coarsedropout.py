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

    width, height = aug_img.shape[1], aug_img.shape[0]
    deleted = 0
    for row_idx in range(y, height):
        for col_idx in range(x, width):
            if np.array_equal(img[row_idx, col_idx], [0, 0, 0]):
                deleted += 1
    aug_p = deleted / (width * height)
    margin = 0.02
    print(aug_p)

    assert aug_p <= (0.1 + margin) and aug_p >= (0.1 - margin)
    assert np.less_equal(
        img, aug_img
    ).all(), "Performing augmentation does not yield expected deleted boxes"
    assert np.array_equal(
        bboxes, aug_bboxes
    ), "Performing augmentation does not yield original augmentation"
