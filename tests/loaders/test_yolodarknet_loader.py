import pytest
import numpy as np

from discolight.annotations import annotations_to_numpy_array


@pytest.mark.usefixtures("yolodarknet_imageset",
                         "yolodarknet_equiv_csv_imageset")
def test_yolodarknet_loader(yolodarknet_imageset,
                            yolodarknet_equiv_csv_imageset):

    for image_name in yolodarknet_equiv_csv_imageset:

        _, yd_annotations = yolodarknet_imageset[image_name]
        _, csv_annotations = yolodarknet_equiv_csv_imageset[image_name]

        yd_bboxes = annotations_to_numpy_array(yd_annotations)
        csv_bboxes = annotations_to_numpy_array(csv_annotations)

        assert np.allclose(
            yd_bboxes, csv_bboxes
        ), "Same bboxes loaded with YOLODarknet, FourCornersCSV not equal." ""
