from abc import ABC, abstractmethod


class ImageLoader(ABC):

    _include_in_factory = True

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def params():
        raise NotImplementedError

    @abstractmethod
    def load_image(self, image_name):
        raise NotImplementedError
