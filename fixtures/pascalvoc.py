import os
from pathlib import Path

import pytest

from discolight.loaders.image.directory import Directory
from discolight.loaders.annotation.fourcornerscsv import FourCornersCSV
from discolight.loaders.annotation.pascalvoc import PascalVOC

fixtures_directory = Path(__file__).resolve().parent


@pytest.fixture
def pascalvoc_imageset():
    with PascalVOC(annotations_folder=os.path.join(
            fixtures_directory, "pascalvoc")) as annotation_loader, Directory(
                directory=os.path.join(fixtures_directory,
                                       "pascalvoc")) as image_loader:
        images = annotation_loader.load_annotated_images(image_loader)

    return images


@pytest.fixture
def pascalvoc_equiv_csv_imageset():
    with FourCornersCSV(
            annotations_file=os.path.join(fixtures_directory, "pascalvoc",
                                          "annotations.csv"),
            normalized=True) as annotation_loader, Directory(
                directory=os.path.join(fixtures_directory,
                                       "pascalvoc")) as image_loader:
        images = annotation_loader.load_annotated_images(image_loader)

    return images


@pytest.fixture
def pascalvoc_additional_values_imageset():
    with PascalVOC(annotations_folder=os.path.join(
            fixtures_directory, "pascalvoc-additionalvalues")
                   ) as annotation_loader, Directory(directory=os.path.join(
                       fixtures_directory, "pascalvoc")) as image_loader:
        images = annotation_loader.load_annotated_images(image_loader)

    return images
