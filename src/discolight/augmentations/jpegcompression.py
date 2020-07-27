"""A JPEG compression augmentation."""
import cv2
from discolight.params.params import Params
from .augmentation.types import ColorAugmentation
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class JpegCompression(ColorAugmentation):
    """JPEG compress the given image."""

    def __init__(self, strength):
        super().__init__()

        self.strength = strength
        self.flag = cv2.IMWRITE_JPEG_QUALITY

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add(
            "strength", "Compression strength between 0 to 100", int, 95
        )

    def augment_img(self, img, _bboxes):
        """Augment an image."""
        # Ensure strength value do not go out of range
        if self.strength < 0:
            self.strength = 0
        elif self.strength > 100:
            self.strength = 100

        _, encoded_img = cv2.imencode(".jpg", img, (self.flag, self.strength))
        compressed_img = cv2.imdecode(encoded_img, cv2.IMREAD_UNCHANGED)

        return compressed_img
