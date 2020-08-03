import pytest
import numpy as np
import random
from discolight.annotations import (annotations_to_numpy_array)
from discolight.augmentations.colortemperature import ColorTemperature

@pytest.mark.usefixtures("sample_image")
def test_my_augmentation_warmer(sample_image):
    img, annotations = sample_image    

    bboxes = annotations_to_numpy_array(annotations)
    
    # Kelvin values smaller than 6600K map to RGB multipliers 
    # acting as warming filters.
    kelvin_input = random.randint(1000, 6560)
    
    augmentation = ColorTemperature(kelvin=kelvin_input)
    
    aug_img, aug_bboxes = augmentation.augment(img.copy(), bboxes.copy())
    
    # Warming filters make reds more intensive and blue less.
    assert np.less_equal(
        img[:,:,0], aug_img[:,:,0]
    ).all(), "Performing augmentation does not yield expected red channel"
    assert np.greater_equal(
        img[:,:,2], aug_img[:,:,2]
    ).all(), "Performing augmentation does not yield expected blue channel"
    assert np.array_equal(
        bboxes, aug_bboxes
    ), "Performing augmentation does not yield original bounding boxes"

def test_my_augmentation_colder():
    img =  np.array(([
        [[ 62, 238, 229],
         [242,  39, 182]],
        [[167, 153,  41],
         [130,  63, 162]]]))
    
    annotations = []

    bboxes = annotations_to_numpy_array(annotations)
    
    # Kelvin values larger than 6600K map to RGB multipliers 
    # acting as cooling filters.
    kelvin_input = random.randint(6710, 40000)
    
    augmentation = ColorTemperature(kelvin=kelvin_input)
    aug_img, aug_bboxes = augmentation.augment(img.copy(), bboxes.copy())
    
    # Cooling filters make blues more intensive and reds less.
    assert np.greater_equal(
        img[:,:,0], aug_img[:,:,0]
    ).all(), "Performing augmentation does not yield expected red channel"
    assert np.less_equal(
        img[:,:,2], aug_img[:,:,2]
    ).all(), "Performing augmentation does not yield expected blue channel"
    assert np.array_equal(
        bboxes, aug_bboxes
    ), "Performing augmentation does not yield original bounding boxes"
