import os
from pathlib import Path

import pytest

from discolight.loaders.image.directory import Directory
from discolight.loaders.annotation.fourcornerscsv import FourCornersCSV
from discolight.loaders.annotation.yolodarknet import YOLODarknet

fixtures_directory = Path(__file__).resolve().parent


@pytest.fixture
def yolodarknet_imageset():
    with YOLODarknet(
            annotations_folder=os.path.join(fixtures_directory, "yolodarknet"),
            image_ext="jpg") as annotation_loader, Directory(
                directory=os.path.join(fixtures_directory,
                                       "yolodarknet")) as image_loader:
        images = annotation_loader.load_annotated_images(image_loader)

    return images


@pytest.fixture
def yolodarknet_equiv_csv_imageset():
    with FourCornersCSV(
            annotations_file=os.path.join(fixtures_directory, "yolodarknet",
                                          "annotations.csv"),
            normalized=True) as annotation_loader, Directory(
                directory=os.path.join(fixtures_directory,
                                       "yolodarknet")) as image_loader:
        images = annotation_loader.load_annotated_images(image_loader)

    return images
