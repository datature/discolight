from discolight.params.params import Params
from .augmentation.types import Augmentation, augmentation_list
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class Sequence(Augmentation):
    def __init__(self, augmentations):
        super().__init__()

        self.augmentations = augmentations

    @staticmethod
    def params():
        return Params().add("augmentations", "", augmentation_list, [])

    def augment(self, img, bboxes):

        for augmentation in self.augmentations:

            img, bboxes = augmentation.augment(img, bboxes)

        return img, bboxes
