import pytest
import numpy as np

from discolight.annotations import annotations_to_numpy_array


@pytest.mark.usefixtures("pascalvoc_imageset", "pascalvoc_equiv_csv_imageset")
def test_pascalvoc_loader(pascalvoc_imageset, pascalvoc_equiv_csv_imageset):

    for image_name in pascalvoc_imageset:

        _, pv_annotations = pascalvoc_imageset[image_name]

        _, csv_annotations = pascalvoc_equiv_csv_imageset[image_name]

        pv_bboxes = annotations_to_numpy_array(pv_annotations)
        csv_bboxes = annotations_to_numpy_array(csv_annotations)

        assert np.allclose(
            pv_bboxes, csv_bboxes
        ), "Same bboxes loaded with PascalVOC, FourCornersCSV are not equal"


@pytest.mark.usefixtures("pascalvoc_additional_values_imageset")
def test_pascalvoc_loader_additional_values(
        pascalvoc_additional_values_imageset):

    _, wheat1_annotations = pascalvoc_additional_values_imageset["wheat1.jpg"]

    annotation = wheat1_annotations[1]

    assert annotation.additional_info["name"] == "test"
    assert annotation.additional_info["truncated"] == "1"
    assert annotation.additional_info["difficult"] == "2"
