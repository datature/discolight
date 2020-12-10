import os
import pytest

from discolight.loaders.image.directory import (Directory as DirectoryLoader)
from discolight.loaders.annotation.coco import (COCO as COCOLoader)

from discolight.writers.image.directory import (Directory as DirectoryWriter)
from discolight.writers.annotation.coco import (COCO as COCOWriter)


@pytest.mark.usefixtures("coco_imageset")
def test_identical_img_bboxes_recovered_using_coco_writer(
        tmp_path, coco_imageset):

    with DirectoryWriter(
            directory=tmp_path,
            clean_directory=False) as image_writer, COCOWriter(
                annotations_file=os.path.join(
                    tmp_path, "annotations.coco.json")) as annotation_writer:

        for image_name in coco_imageset:

            image, annotations = coco_imageset[image_name]

            image_writer.write_image(image_name, image)
            annotation_writer.write_annotations_for_image(
                image_name, image, annotations)

    with DirectoryLoader(directory=tmp_path) as image_loader, COCOLoader(
            annotations_file=os.path.join(
                tmp_path, "annotations.coco.json")) as annotation_loader:

        loaded_images = annotation_loader.load_annotated_images(image_loader)

    for image_name in loaded_images:

        _, loaded_annotations = loaded_images[image_name]
        _, annotations = coco_imageset[image_name]

        for annotation, loaded_annotation in zip(annotations,
                                                 loaded_annotations):

            assert annotation.x_min == loaded_annotation.x_min
            assert annotation.y_min == loaded_annotation.y_min
            assert annotation.x_max == loaded_annotation.x_max
            assert annotation.y_max == loaded_annotation.y_max
            assert annotation.class_idx == loaded_annotation.class_idx

            assert annotation.additional_info["image_license"][
                "url"] == loaded_annotation.additional_info["image_license"][
                    "url"]
            assert annotation.additional_info["image_license"][
                "name"] == loaded_annotation.additional_info["image_license"][
                    "name"]

            assert annotation.additional_info["category"][
                "name"] == loaded_annotation.additional_info["category"][
                    "name"]
            assert annotation.additional_info["category"][
                "supercategory"] == loaded_annotation.additional_info[
                    "category"]["supercategory"]
