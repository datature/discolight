"""A Image compression augmentation."""
import cv2
from discolight.params.params import Params
from .augmentation.types import ColorAugmentation, BoundedNumber
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class ImageCompression(ColorAugmentation):

    """Apply a compression effect to the given image.

    This function is a lossy JPEG compression operation.
    """

    def __init__(self, strength):
        """Construct a ImageCompression augmentation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        super().__init__()
        self.strength = strength

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add(
            "strength", "Compression strength", BoundedNumber(int, 0, 100), 1,
        )

    def augment_img(self, img, _bboxes):
        """Augment an image."""
        _, encoded_img = cv2.imencode(
            ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), int(self.strength)]
        )
        compressed_img = cv2.imdecode(encoded_img, cv2.IMREAD_UNCHANGED)

        return compressed_img
