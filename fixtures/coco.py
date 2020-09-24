import os
from pathlib import Path

import pytest

from discolight.loaders.image.directory import Directory
from discolight.loaders.annotation.fourcornerscsv import FourCornersCSV
from discolight.loaders.annotation.coco import COCO

fixtures_directory = Path(__file__).resolve().parent


@pytest.fixture
def coco_imageset():
    with COCO(annotations_file=os.path.join(fixtures_directory, "coco",
                                            "annotations.coco.json")
              ) as annotation_loader, Directory(directory=os.path.join(
                  fixtures_directory, "coco")) as image_loader:
        images = annotation_loader.load_annotated_images(image_loader)

    return images


@pytest.fixture
def coco_equiv_csv_imageset():
    with FourCornersCSV(annotations_file=os.path.join(fixtures_directory,
                                                      "coco",
                                                      "annotations.csv"),
                        normalized=True) as annotation_loader, Directory(
                            directory=os.path.join(fixtures_directory,
                                                   "coco")) as image_loader:
        images = annotation_loader.load_annotated_images(image_loader)

    return images
