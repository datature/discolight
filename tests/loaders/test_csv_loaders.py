import pytest
import numpy as np

from discolight.annotations import annotations_to_numpy_array


@pytest.mark.usefixtures("sample_image", "sample_image_wh_bboxes")
def test_four_corners_width_height_equivalent(sample_image,
                                              sample_image_wh_bboxes):

    img_fc, annot_fc = sample_image

    img_wh, annot_wh = sample_image_wh_bboxes

    assert np.array_equal(
        img_fc, img_wh
    ), "Same image loaded with FourCornersCSV and WidthHeightCSV is not equal"

    bboxes_fc = annotations_to_numpy_array(annot_fc)
    bboxes_wh = annotations_to_numpy_array(annot_wh)

    assert np.allclose(
        bboxes_fc, bboxes_wh
    ), "Same bboxes loaded with FourCornersCSV, WidthHeightCSV are not equal"
