import os
from discolight.writers.image.directory import Directory


def test_directory_image_writer_clean_directory_true(tmp_path):

    with open(os.path.join(tmp_path, "test"), "w") as test_file:
        test_file.write("test")

    with Directory(directory=tmp_path, clean_directory=True):
        assert os.path.isfile(os.path.join(tmp_path, "test")) is False


def test_directory_image_writer_clean_directory_false(tmp_path):

    with open(os.path.join(tmp_path, "test"), "w") as test_file:
        test_file.write("test")

    with Directory(directory=tmp_path, clean_directory=False):
        assert os.path.isfile(os.path.join(tmp_path, "test"))
