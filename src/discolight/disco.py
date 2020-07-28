"""An easy-to-use library interface for Discolight."""
from .augmentations.augmentation.types import Augmentation
from .augmentations.factory import (make_augmentations_factory,
                                    get_augmentations_set)
from .annotations import (annotations_from_numpy_array,
                          annotations_to_numpy_array)


class DiscolightInterface:

    """A class that makes it easy to construct and perform augmentations.

    Once instantiated, accessing a property A as a method will construct an
    augmentation that can be applied to an image and a set of annotations.

    For example, to construct a GrayScale augmentation:

       aug = disco.GrayScale()

    or, with parameters:

       aug = disco.GrayScale(probs=0.7)

    Now aug is an instance of a CallableAugmentation object. It can be applied
    to an image (and optionally, a set of bounding boxes):

       image = load_image(...)
       aug_img = aug(image)

       image = load_image(...)
       annotations = [...]

       aug_img, aug_annotations = aug(image, annotations)

    If specified, the annotations should be an array of BoundingBox objects.
    Returned annotations will also be an array of BoundingBox objects.

    CallableAugmentation objects can also be supplied as parameters to other
    augmentations, such as a Sequence augmentation:

        seq = disco.Sequence(augmentations=[
            disco.GrayScale(),
            ...
        ])

        image = load_image(...)
        aug_img = seq(image)
    """

    def __init__(self):
        """Construct a new Discolight interface object."""
        self._aug_set = get_augmentations_set()
        self._factory = make_augmentations_factory()

    def __getattr__(self, name):
        """Return a function to construct an augmenation."""
        if name not in self._aug_set:
            raise AttributeError("No such augmentation {}".format(name))

        def make_augmentation(**params):

            augmentation = self._factory(name, **params)

            # This is a bit of a trick. We want the augmentation object to be
            # callable as a function to augment an image and annotations, but
            # also to be an instance of the Augmentation class so that it can
            # be passed as a parameter to augmentations like Sequence. To
            # achieve both of these goals, we construct a new class that
            # inherits from Augmentation, but implements the __call__ magic
            # method so that it can be invoked as a function by a user of the
            # Discolight library.

            # We construct it here in the closure instead of at top-level
            # because we need access to the constructed augmentation in
            # the static params() method, so we can't just pass it to the
            # constructor.

            class CallableAugmentation(Augmentation):

                """An augmentation that can be invoked as a function."""

                def __init__(self):
                    """Construct a new callable augmentation."""
                    self.augmentation = augmentation

                @staticmethod
                def params():
                    """Return the parameters for this augmenation."""
                    return augmentation.params()

                def augment(self, img, bboxes):
                    """Perform the given augmentation."""
                    return self.augmentation.augment(img, bboxes)

                def __call__(self, image, annotations=None):
                    """Perform the given augmentation.

                    This method is invoked when you invoke an instance of
                    this class as a function. Unlike the augment method,
                    annotations can be optionally passed as a list of
                    BoundingBox objects (conversion to and from the numpy
                    array format is handled for you).
                    """
                    if annotations is None:
                        return self.augmentation.get_img(image.copy())

                    bboxes = annotations_to_numpy_array(annotations)

                    aug_img, aug_bboxes = self.augmentation.augment(
                        image.copy(), bboxes.copy())

                    return aug_img, annotations_from_numpy_array(aug_bboxes)

            return CallableAugmentation()

        return make_augmentation


disco = DiscolightInterface()
