import os
import pytest

from discolight.run import main


@pytest.mark.usefixtures("query_bad_bboxes")
def test_augmentor_raises_error_on_bad_bboxes(query_bad_bboxes, tmp_path):

    with open(os.path.join(tmp_path, "query.yml"), "w") as query_file:
        query_file.write(query_bad_bboxes)

        with pytest.raises(ValueError):
            main(['generate', os.path.join(tmp_path, "query.yml")])
