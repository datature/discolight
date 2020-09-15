import os
import pytest

from discolight.loaders.image.directory import (Directory as DirectoryLoader)
from discolight.loaders.annotation.yolokeras import (YOLOKeras as
                                                     YOLOKerasLoader)

from discolight.writers.image.directory import (Directory as DirectoryWriter)
from discolight.writers.annotation.yolokeras import (YOLOKeras as
                                                     YOLOKerasWriter)


@pytest.mark.usefixtures("yolokeras_imageset")
def test_identical_img_bboxes_recovered_using_yolo_keras_writer(
        tmp_path, yolokeras_imageset):

    with DirectoryWriter(
            directory=tmp_path,
            clean_directory=False) as image_writer, YOLOKerasWriter(
                annotations_file=os.path.join(
                    tmp_path, "annotations.txt")) as annotation_writer:

        for image_name in yolokeras_imageset:

            image, annotations = yolokeras_imageset[image_name]

            image_writer.write_image(image_name, image)
            annotation_writer.write_annotations_for_image(
                image_name, image, annotations)

    with DirectoryLoader(directory=tmp_path) as image_loader, YOLOKerasLoader(
            annotations_file=os.path.join(
                tmp_path, "annotations.txt")) as annotation_loader:

        loaded_images = annotation_loader.load_annotated_images(image_loader)

    for image_name in loaded_images:

        _, loaded_annotations = loaded_images[image_name]
        _, annotations = yolokeras_imageset[image_name]

        for annotation, loaded_annotation in zip(annotations,
                                                 loaded_annotations):

            assert annotation.x_min == loaded_annotation.x_min
            assert annotation.y_min == loaded_annotation.y_min
            assert annotation.x_max == loaded_annotation.x_max
            assert annotation.y_max == loaded_annotation.y_max
            assert annotation.class_idx == loaded_annotation.class_idx
