import random
import numpy as np
import pytest

from discolight.annotations import annotations_to_numpy_array
from discolight.augmentations.oneof import OneOf


class MockAugmentation():

    def __init__(self):

        self.times_called = 0

    @staticmethod
    def params():
        return None

    def augment(self, img, bboxes):

        self.times_called += 1

        return img, bboxes


@pytest.mark.usefixtures("sample_image")
def test_one_of_no_augmentations(sample_image):
    img, annotations = sample_image

    bboxes = annotations_to_numpy_array(annotations)

    augmentation = OneOf(augmentations=[])

    aug_img, aug_bboxes = augmentation.augment(img.copy(), bboxes.copy())

    assert np.array_equal(img, aug_img)
    assert np.array_equal(bboxes, aug_bboxes)


def test_one_of_calls_only_one():

    def generate_mock_augmentations(n):

        num_augmentations = random.randint(2, n)
        augmentations = []

        for _ in range(num_augmentations):
            augmentations.append(MockAugmentation())

        return augmentations

    for _ in range(10000):

        augmentations = generate_mock_augmentations(10)

        one_of = OneOf(augmentations=augmentations)

        one_of.augment(None, None)

        assert sum([mock.times_called for mock in augmentations]) == 1
