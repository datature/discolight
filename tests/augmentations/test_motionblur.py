import pytest
import numpy as np

from discolight.annotations import (annotations_to_numpy_array)
from discolight.augmentations.motionblur import motionblur

@pytest.mark.usefixtures("sample_image")
def test_motionblur(sample_image):
	
	
	img, annotations = sample_image
	
	bboxes = annotations_to_numpy_array(annotations)
	
	augmentation = motionblur(kernel_size=10,direction='DOWN')
	
	aug_img, aug_bboxes = augmentation.augment(img.copy(), bboxes.copy())
	
	assert np.array_equal(bboxes,aug_bboxes)
<<<<<<< HEAD
	assert np.array_equal(img.shape,aug_img.shape)
=======
    	assert np.equal(img.shape,aug_img.shape)
>>>>>>> 17b1fa2e4972c11db2be1d48bdd209d4d5f3abeb
    
    
