from abc import ABC, abstractmethod


class ImageWriter(ABC):

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
    def write_image(self, image_name, image):
        raise NotImplementedError
