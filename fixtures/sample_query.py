# flake8: noqa=E501
from pathlib import Path

import pytest

fixtures_directory = Path(__file__).resolve().parent


@pytest.fixture
def sample_query(tmp_path):
    return """
input:
  images:
    loader: Directory
    options:
      directory: {fixtures_directory}/augmentor

  annotations:
    loader: FourCornersCSV
    options:
      annotations_file: {fixtures_directory}/augmentor/annotations.csv
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
  - name: Sequence
    options:
      augmentations:
        - name: Rotate
        - name: GrayScale
        - name: Sequence
          options:
            augmentations:
              - name: Shear
              - name: GaussianNoise
                options:
                  mean: 0.3
  - name: Rotate
    options:
      probs: 0.7
      angle: 35
  - name: GaussianNoise
    options:
      probs: 0.9
  - name: Shear
  - name: Translate
  - name: VerticalFlip
save-original: true # Whether to save the original images to the output folder
save-bbox: true # Whether bounding boxes should be drawn on the augmented images
""".format(fixtures_directory=fixtures_directory, tmp_path=tmp_path)
