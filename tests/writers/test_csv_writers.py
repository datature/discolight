import os
import pytest
import numpy as np

from discolight.annotations import annotations_to_numpy_array
from discolight.loaders.image.directory import (Directory as DirectoryLoader)
from discolight.loaders.annotation.fourcornerscsv import (FourCornersCSV as
                                                          FourCornersCSVLoader)
from discolight.loaders.annotation.widthheightcsv import (WidthHeightCSV as
                                                          WidthHeightCSVLoader)
from discolight.writers.image.directory import (Directory as DirectoryWriter)
from discolight.writers.annotation.fourcornerscsv import (FourCornersCSV as
                                                          FourCornersCSVWriter)
from discolight.writers.annotation.widthheightcsv import (WidthHeightCSV as
                                                          WidthHeightCSVWriter)


@pytest.mark.usefixtures("sample_image")
@pytest.mark.parametrize("annot_loader,annot_writer",
                         [(FourCornersCSVLoader, FourCornersCSVWriter),
                          (WidthHeightCSVLoader, WidthHeightCSVWriter)],
                         ids=["FourCornersCSV", "WidthHeightCSV"])
@pytest.mark.parametrize("normalized", [True, False],
                         ids=["normalized", "unnormalized"])
def test_identical_img_bboxes_recovered_using_csv_writer(
        tmp_path, sample_image, annot_loader, normalized, annot_writer):

    img, annotations = sample_image

    bboxes = annotations_to_numpy_array(annotations)

    with DirectoryWriter(directory=tmp_path,
                         clean_directory=False) as image_writer, annot_writer(
                             annotations_file=os.path.join(
                                 tmp_path, "annot.csv"),
                             normalized=normalized) as annotation_writer:

        image_writer.write_image("image.jpg", img)

        annotation_writer.write_annotations_for_image("image.jpg", img,
                                                      annotations)

    with DirectoryLoader(directory=tmp_path) as image_loader, annot_loader(
            annotations_file=os.path.join(tmp_path, "annot.csv"),
            normalized=normalized) as annotation_loader:

        images = annotation_loader.load_annotated_images(image_loader)

    _, loaded_annotations = images["image.jpg"]

    loaded_bboxes = annotations_to_numpy_array(loaded_annotations)

    assert np.allclose(bboxes,
                       loaded_bboxes), "Annotations not the same after writing"
