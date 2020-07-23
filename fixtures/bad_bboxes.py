# flake8: noqa=E501
from pathlib import Path

import pytest

fixtures_directory = Path(__file__).resolve().parent


@pytest.fixture(params=[
    "annotations-bbox-below-0.csv", "annotations-bbox-greater-img-height.csv",
    "annotations-bbox-greater-img-width.csv"
])
def query_bad_bboxes(tmp_path, request):
    return """
input:
  images:
    loader: Directory
    options:
      directory: {fixtures_directory}/augmentor

  annotations:
    loader: FourCornersCSV
    options:
      annotations_file: {fixtures_directory}/augmentor/{csv_file}
      normalized: true
output:
  images:
    writer: Directory
    options:
      directory: {tmp_path}
      clean_directory: false
  annotations:
    writer: FourCornersCSV
    options:
      annotations_file: {tmp_path}/aug_annotations.csv
      normalized: true
augmentations:
  - name: HorizontalFlip
    options: {{}}
save-original: true # Whether to save the original images to the output folder
save-bbox: true # Whether bounding boxes should be drawn on the augmented images
""".format(fixtures_directory=fixtures_directory,
           tmp_path=tmp_path,
           csv_file=request.param)
