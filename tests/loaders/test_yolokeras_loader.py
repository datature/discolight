import pytest
import numpy as np

from discolight.annotations import annotations_to_numpy_array


@pytest.mark.usefixtures("yolokeras_imageset", "yolokeras_equiv_csv_imageset")
def test_yolokeras_loader(yolokeras_imageset, yolokeras_equiv_csv_imageset):

    for image_name in yolokeras_equiv_csv_imageset:

        _, yk_annotations = yolokeras_imageset[image_name]
        _, csv_annotations = yolokeras_equiv_csv_imageset[image_name]

        yk_bboxes = annotations_to_numpy_array(yk_annotations)
        csv_bboxes = annotations_to_numpy_array(csv_annotations)

        assert np.allclose(
            yk_bboxes, csv_bboxes
        ), "Same bboxes loaded with YOLOKeras, FourCornersCSV not equal." ""
