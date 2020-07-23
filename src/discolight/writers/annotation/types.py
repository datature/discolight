from abc import ABC, abstractmethod
import csv
from discolight.params.params import Params


class AnnotationWriter(ABC):

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
    def write_annotations_for_image(self, image_name, image, annotations):
        raise NotImplementedError


class CSVAnnotationWriter(AnnotationWriter):
    def __init__(self, annotations_file, normalized):

        self.annotations_file = annotations_file
        self.normalized = normalized

        self.annotations_fp = None
        self.writer = None

    @abstractmethod
    def get_csv_fieldnames(self):
        raise NotImplementedError

    def __enter__(self):
        self.annotations_fp = open(self.annotations_file, "w", newline='')
        self.writer = csv.DictWriter(self.annotations_fp,
                                     self.get_csv_fieldnames())

        self.writer.writeheader()

        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        self.annotations_fp.close()

    @staticmethod
    def params():
        return Params().add(
            "annotations_file",
            "The path to the CSV file to write the annotations to", str, "",
            True
        ).add(
            "normalized",
            "whether the bounding box coordinates should be normalized before "
            "saving", bool, True)

    @abstractmethod
    def get_csv_row(self, image_name, image, annotation):
        raise NotImplementedError

    def write_annotations_for_image(self, image_name, image, annotations):

        for annotation in annotations:

            processed_annotation = annotation
            if self.normalized:
                height, width, _ = image.shape
                processed_annotation = annotation.normalize(width, height)

            self.writer.writerow(
                self.get_csv_row(image_name, image, processed_annotation))
