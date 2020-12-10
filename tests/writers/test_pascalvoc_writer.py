import pytest

from discolight.loaders.image.directory import (Directory as DirectoryLoader)
from discolight.loaders.annotation.pascalvoc import (PascalVOC as
                                                     PascalVOCLoader)

from discolight.writers.image.directory import (Directory as DirectoryWriter)
from discolight.writers.annotation.pascalvoc import (PascalVOC as
                                                     PascalVOCWriter)


@pytest.mark.usefixtures("pascalvoc_additional_values_imageset")
def test_identical_img_bboxes_recovered_using_pascal_voc_writer(
        tmp_path, pascalvoc_additional_values_imageset):

    with DirectoryWriter(
            directory=tmp_path,
            clean_directory=False) as image_writer, PascalVOCWriter(
                annotations_folder=tmp_path,
                clean_directory=False,
                database='') as annotation_writer:

        for image_name in pascalvoc_additional_values_imageset:

            image, annotations = pascalvoc_additional_values_imageset[
                image_name]

            image_writer.write_image(image_name, image)
            annotation_writer.write_annotations_for_image(
                image_name, image, annotations)

    with DirectoryLoader(directory=tmp_path) as image_loader, PascalVOCLoader(
            annotations_folder=tmp_path) as annotation_loader:

        loaded_images = annotation_loader.load_annotated_images(image_loader)

    for image_name in loaded_images:

        _, loaded_annotations = loaded_images[image_name]
        _, annotations = pascalvoc_additional_values_imageset[image_name]

        for annotation, loaded_annotation in zip(annotations,
                                                 loaded_annotations):

            assert annotation.x_min == loaded_annotation.x_min
            assert annotation.y_min == loaded_annotation.y_min
            assert annotation.x_max == loaded_annotation.x_max
            assert annotation.y_max == loaded_annotation.y_max
            assert annotation.class_idx == loaded_annotation.class_idx

            for prop in annotation.additional_info:

                annotation_prop = annotation.additional_info[prop]
                loaded_annotation_prop = loaded_annotation.additional_info[
                    prop]

                assert annotation_prop == loaded_annotation_prop
