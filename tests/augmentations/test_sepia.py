import pytest
import numpy as np

from discolight.annotations import (annotations_to_numpy_array)
from discolight.augmentations.sepia import Sepia

def test_my_augmentation_sepia():
    img =  np.array(([
        [[ 62, 238, 229],
         [242,  39, 182]],
        [[167, 153,  41],
         [130,  63, 162]]]))
    
    annotations = []
    
    # Values calculated by hand using formula from <https://www.techrepublic.com/blog/how-do-i/how-do-i-convert-images-to-grayscale-and-sepia-tone-using-c/>
    expected_red = np.array([[250, 159], [191, 130]])
    expected_green = np.array([[223, 141], [170, 115]])
    expected_blue = np.array([[173, 110], [132, 90]])
    expected_aug_img = np.zeros(img.shape, dtype=np.uint8)
    expected_aug_img[:, :, 0] = expected_red
    expected_aug_img[:, :, 1] = expected_green
    expected_aug_img[:, :, 2] = expected_blue
    
    bboxes = annotations_to_numpy_array(annotations)
    
    augmentation = Sepia()
    
    aug_img, aug_bboxes = augmentation.augment(img.copy(), bboxes.copy())
    
    assert np.allclose(
        expected_aug_img, aug_img
    ), "Performing augmentation does not yield expected image"
    assert np.array_equal(
        bboxes, aug_bboxes
    ), "Performing augmentation does not yield original augmentation"
    