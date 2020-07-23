import pytest
import numpy as np

from discolight.annotations import (annotations_to_numpy_array)
from discolight.augmentations.horizontalflip import HorizontalFlip
from discolight.augmentations.verticalflip import VerticalFlip


@pytest.mark.usefixtures("sample_image")
@pytest.mark.parametrize("augmentation", [HorizontalFlip(), VerticalFlip()])
def test_augmentation_is_involution(augmentation, sample_image):

    img, annotations = sample_image

    bboxes = annotations_to_numpy_array(annotations)

    aug_img, aug_bboxes = augmentation.augment(img.copy(), bboxes.copy())

    re_aug_img, re_aug_bboxes = augmentation.augment(aug_img.copy(),
                                                     aug_bboxes.copy())

    assert np.allclose(
        img, re_aug_img
    ), "Performing augmentation twice does not yield origial image"
    assert np.allclose(
        bboxes, re_aug_bboxes
    ), "Performing augmentation twice does not yield original annotations"
