import pytest
import numpy as np

from discolight.annotations import (annotations_to_numpy_array)
from discolight.augmentations.motionblur import motionblur

@pytest.mark.usefixtures("sample_image")
def test_motionblur(sample_image):
	
	img, annotations = sample_image
	
	bboxes = annotations_to_numpy_array(annotations)
	
	augmentation = motionblur()
	
	aug_img, aug_bboxes = augmentation.augment(img.copy(), bboxes.copy())
	
	assert np.array_equal(bboxes,aug_bboxes)
    	assert np.equal(img.shape,aug_img.shape)
    
    
