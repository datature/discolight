import os
import shutil
import random
from filecmp import dircmp
import pytest
from discolight.run import main


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

    cmp_result = dircmp(tmp_path, "./snapshots/run")

    assert len(cmp_result.left_only) == 0
    assert len(cmp_result.right_only) == 0
    assert len(cmp_result.diff_files) == 0
