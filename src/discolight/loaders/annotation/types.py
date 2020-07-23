from abc import ABC, abstractmethod
import csv
from collections import namedtuple
from discolight.params.params import Params
from discolight.annotations import ImageWithAnnotations


class AnnotationLoader(ABC):

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
    def load_annotated_images(self, image_loader):
        raise NotImplementedError


CSVRow = namedtuple('CSVRow', 'image_name bbox')


class CSVAnnotationLoader(AnnotationLoader):
    def __init__(self, annotations_file, normalized):

        self.annotations_file = annotations_file
        self.normalized = normalized

        self.annotations_fp = None

    def __enter__(self):
        self.annotations_fp = open(self.annotations_file, "r", newline='')
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        self.annotations_fp.close()

    @staticmethod
    def params():
        return Params().add(
            "annotations_file",
            "The path to the CSV file containing the annotations", str, "",
            True
        ).add(
            "normalized",
            "whether the bounding box coordinates are stored in a normalized "
            "format", bool, True)

    @abstractmethod
    def get_csv_row(self, row):
        raise NotImplementedError

    def load_annotated_images(self, image_loader):

        images = {}

        reader = csv.DictReader(self.annotations_fp, skipinitialspace=True)

        for row in reader:

            csv_row = self.get_csv_row(row)

            if csv_row.image_name in images:
                if self.normalized:
                    height, width, _ = images[csv_row.image_name].image.shape

                    images[csv_row.image_name].bboxes.append(
                        csv_row.bbox.unnormalize(width, height))
                    continue

                images[csv_row.image_name].bboxes.append(csv_row.bbox)
                continue

            image = image_loader.load_image(csv_row.image_name)

            annotation = csv_row.bbox
            if self.normalized:
                height, width, _ = image.shape
                annotation = csv_row.bbox.unnormalize(width, height)

            images[csv_row.image_name] = ImageWithAnnotations(
                image=image_loader.load_image(csv_row.image_name),
                bboxes=[annotation])

        return images
