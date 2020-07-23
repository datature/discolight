import os
from pathlib import Path

import pytest

from discolight.loaders.image.directory import Directory
from discolight.loaders.annotation.fourcornerscsv import FourCornersCSV
from discolight.loaders.annotation.widthheightcsv import WidthHeightCSV

fixtures_directory = Path(__file__).resolve().parent


@pytest.fixture
def sample_image():
    with FourCornersCSV(annotations_file=os.path.join(fixtures_directory,
                                                      "annotations.csv"),
                        normalized=True) as annotation_loader, Directory(
                            directory=fixtures_directory) as image_loader:

        images = annotation_loader.load_annotated_images(image_loader)

    return images["wheat1.jpg"]


@pytest.fixture
def sample_image_wh_bboxes():
    with WidthHeightCSV(annotations_file=os.path.join(fixtures_directory,
                                                      "annotations-wh.csv"),
                        normalized=True) as annotation_loader, Directory(
                            directory=fixtures_directory) as image_loader:

        images = annotation_loader.load_annotated_images(image_loader)

    return images["wheat1.jpg"]
