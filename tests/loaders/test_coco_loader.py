import pytest
import numpy as np

from discolight.annotations import annotations_to_numpy_array


@pytest.mark.usefixtures("coco_imageset", "coco_equiv_csv_imageset")
def test_coco_loader(coco_imageset, coco_equiv_csv_imageset):

    for image_name in coco_equiv_csv_imageset:

        _, cc_annotations = coco_imageset[image_name]
        _, csv_annotations = coco_equiv_csv_imageset[image_name]

        cc_bboxes = annotations_to_numpy_array(cc_annotations)
        csv_bboxes = annotations_to_numpy_array(csv_annotations)

        assert np.allclose(
            cc_bboxes, csv_bboxes
        ), "Same bboxes loaded with COCO, FourCornersCSV not equal." ""
