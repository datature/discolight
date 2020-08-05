import numpy as np
import cv2
from discolight.params.params import Params
from .augmentation.types import Augmentation
from .decorators.accepts_probs import accepts_probs

@accepts_probs
class motionblur(Augmentation):
	"""Augmentation description"""
	
	def __init__(self, kernel_size, direction):
		super().__init__()
		
		self.kernel_size = kernel_size
		self.direction = direction
	
	@staticmethod
	def params():
		return Params().add("kernel_size", "Specify the kernel size, greater the size, the more the motion", int, 10).add(
			"direction", "direction in which the blur is pointer towards", str, 'DOWN')

	def augment(self, img, bboxes):
         
            kernel = np.zeros((self.kernel_size, self.kernel_size))
            diag=np.diag_indices(self.kernel_size)

            if self.direction=='DOWN':
                kernel[:, int((self.kernel_size - 1)/2)] = np.ones(self.kernel_size)
                kernel /= self.kernel_size
                new_img = cv2.filter2D(img, -1, kernel)
            elif self.direction=='UP':
                img_rotate_180 = cv2.rotate(img, cv2.ROTATE_180)
                kernel[:, int((self.kernel_size - 1)/2)] = np.ones(self.kernel_size)
                kernel /= self.kernel_size
                up = cv2.filter2D(img_rotate_180, -1, kernel)
                new_img= cv2.rotate(up, cv2.ROTATE_180)
            elif self.direction=='LEFT':
                kernel[int((self.kernel_size - 1)/2), :] = np.ones(self.kernel_size)
                kernel /= self.kernel_size
                new_img = cv2.filter2D(img, -1, kernel)
            elif self.direction=='RIGHT':
                img_rotate_180 = cv2.rotate(img, cv2.ROTATE_180)
                kernel[int((self.kernel_size - 1)/2), :] = np.ones(self.kernel_size)
                kernel /= self.kernel_size
                right= cv2.filter2D(img_rotate_180, -1, kernel)
                new_img = cv2.rotate(right, cv2.ROTATE_180)
            elif self.direction=='TOP_LEFT':
                ind=np.diag_indices(self.kernel_size)
                kernel[ind]=np.ones(self.kernel_size)
                kernel /= self.kernel_size
                new_img = cv2.filter2D(img, -1, kernel)
            elif self.direction=='BOTTOM_RIGHT':
                img_rotate_90_clockwise = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
                ind=np.diag_indices(self.kernel_size)
                kernel[ind]=np.ones(self.kernel_size)
                kernel=np.flip(kernel,axis=1)
                kernel /= self.kernel_size
                bottom_right = cv2.filter2D(img_rotate_90_clockwise, -1, kernel)
                new_img = cv2.rotate(bottom_right, cv2.ROTATE_90_COUNTERCLOCKWISE)
            elif self.direction=='TOP_RIGHT':
                img_rotate_90_clockwise = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
                ind=np.diag_indices(self.kernel_size)
                kernel[ind]=np.ones(self.kernel_size)
                kernel /=self.kernel_size
                top_right=cv2.filter2D(img_rotate_90_clockwise,-1,kernel)
                new_img=cv2.rotate(top_right, cv2.ROTATE_90_COUNTERCLOCKWISE)
            elif self.direction=='BOTTOM_LEFT':
                ind=np.diag_indices(self.kernel_size)
                kernel[ind]=np.ones(self.kernel_size)
                kernel=np.flip(kernel,axis=1)
                kernel /=self.kernel_size
                new_img= cv2.filter2D(img, -1, kernel)

            return new_img, bboxes
