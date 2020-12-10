import os
import shutil
import random
import pytest
import numpy as np
from discolight.run import main

from discolight.loaders.image.directory import Directory
from discolight.loaders.annotation.fourcornerscsv import FourCornersCSV
from discolight.annotations import annotations_to_numpy_array


@pytest.mark.usefixtures("sample_query")
def test_run(snapshot, sample_query, tmp_path):

    random.seed(1)

    with open(os.path.join(tmp_path, "query.yml"), "w") as query_file:
        query_file.write(sample_query)

    main(['generate', os.path.join(tmp_path, "query.yml")])
    os.remove(os.path.join(tmp_path, "query.yml"))

    if snapshot["update_snapshots"]:

        if os.path.isdir("./snapshots/run"):
            shutil.rmtree("./snapshots/run")

        shutil.copytree(tmp_path, "./snapshots/run")
        return

    with FourCornersCSV(annotations_file="./snapshots/run/aug_annotations.csv",
                        normalized=True) as annotation_loader, Directory(
                            directory="./snapshots/run") as image_loader:
        snapshot_images = annotation_loader.load_annotated_images(image_loader)

    with FourCornersCSV(annotations_file=os.path.join(tmp_path,
                                                      "aug_annotations.csv"),
                        normalized=True) as annotation_loader, Directory(
                            directory=tmp_path) as image_loader:
        run_images = annotation_loader.load_annotated_images(image_loader)

    for image_name in snapshot_images:

        snapshot_image, snapshot_annot = snapshot_images[image_name]
        run_image, run_annot = run_images[image_name]

        snapshot_bboxes = annotations_to_numpy_array(snapshot_annot)
        run_bboxes = annotations_to_numpy_array(run_annot)

        assert np.allclose(
            snapshot_image,
            run_image), "Image for {} differs".format(image_name)
        assert np.allclose(
            snapshot_bboxes,
            run_bboxes), "Bounding boxes for {} differ".format(image_name)

    for image_name in run_images:

        if image_name not in snapshot_images:
            assert False, "Image {} not in snapshot".format(image_name)
