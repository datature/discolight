import numpy as np
import cv2
from discolight.params.params import Params
from .augmentation.types import Augmentation
from .decorators.accepts_probs import accepts_probs

@accepts_probs
class motionblur(Augmentation):
	"""Augmentation description"""
	
	def __init__(self, kernel_size, dirn):
		super().__init__()
		
		self.kernel_size = kernel_size
		self.dirn = dirn
	
	@staticmethod
	def params():
		return Params.add("kernel_size", "Specify the kernel size, greater the size, the more the motion", int, 10).add(
			"direction", "direction in which the blur is pointer towards", str, 'DOWN')
    # [LEFT, RIGHT, TOP, DOWN, TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM, RIGHT]
#     .ensure(
# 				lambda params: params["param2"] < 3.0,
# 				"param2 must be less than 3.0")
    
	def augment(self, img, bboxes):		
        
        kernel = np.zeros((kernel_size, kernel_size))
        diag=np.diag_indices(kernel_size)
        
        if self.dirn=='DOWN':
            kernel[:, int((kernel_size - 1)/2)] = np.ones(kernel_size)
            kernel /= kernel_size
            new_img = cv2.filter2D(img, -1, kernel_v)
        elif self.dirn=='LEFT':
            kernel[int((kernel_size - 1)/2), :] = np.ones(kernel_size)
            kernel /= kernel_size
            new_img = cv2.filter2D(img, -1, kernel_v)
        if self.dirn=='TOP_LEFT':
            kernel_v[diag]=np.ones(kernel_size) 
            kernel /= kernel_size
            new_img = cv2.filter2D(img, -1, kernel_v)
 
		return new_img, bboxes