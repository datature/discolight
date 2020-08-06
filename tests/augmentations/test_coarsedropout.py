import pytest
import numpy as np

from discolight.annotations import (annotations_to_numpy_array)
from discolight.augmentations.coarsedropout import CoarseDropout


@pytest.mark.usefixtures("sample_image")
def test_coarsedropout(sample_image):

    img, annotations = sample_image

    bboxes = annotations_to_numpy_array(annotations)

    augmentation = CoarseDropout(deleted_area=0.1, num_rectangles=25)

    aug_img, aug_bboxes = augmentation.augment(img.copy(), bboxes.copy())

    width, height = aug_img.shape[1], aug_img.shape[0]
    deleted_area = 0
    for row_idx in range(0, height):
        for col_idx in range(0, width):
            if np.array_equal(aug_img[row_idx, col_idx], [0, 0, 0]):
                deleted_area += 1
    aug_p = deleted_area / (width * height)
    margin = 0.02
    print(aug_p)

    assert aug_p <= (
        0.1 + margin) and aug_p >= (
            0.1 - margin
    ), "Performing augmentation does not yield expected erased area"
    assert np.array_equal(
        bboxes, aug_bboxes
    ), "Performing augmentation does not yield original augmentation"
