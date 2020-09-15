import os
from pathlib import Path

import pytest

from discolight.loaders.image.directory import Directory
from discolight.loaders.annotation.fourcornerscsv import FourCornersCSV
from discolight.loaders.annotation.yolokeras import YOLOKeras

fixtures_directory = Path(__file__).resolve().parent


@pytest.fixture
def yolokeras_imageset():
    with YOLOKeras(annotations_file=os.path.join(
            fixtures_directory, "yolokeras", "annotations.txt")
                   ) as annotation_loader, Directory(directory=os.path.join(
                       fixtures_directory, "yolokeras")) as image_loader:
        images = annotation_loader.load_annotated_images(image_loader)

    return images


@pytest.fixture
def yolokeras_equiv_csv_imageset():
    with FourCornersCSV(
            annotations_file=os.path.join(fixtures_directory, "yolokeras",
                                          "annotations.csv"),
            normalized=True) as annotation_loader, Directory(
                directory=os.path.join(fixtures_directory,
                                       "yolokeras")) as image_loader:
        images = annotation_loader.load_annotated_images(image_loader)

    return images
