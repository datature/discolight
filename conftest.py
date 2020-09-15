from fixtures.sample_image import sample_image, sample_image_wh_bboxes
from fixtures.pascalvoc import (pascalvoc_imageset,
                                pascalvoc_equiv_csv_imageset,
                                pascalvoc_additional_values_imageset)
from fixtures.yolodarknet import (yolodarknet_imageset,
                                  yolodarknet_equiv_csv_imageset)
from fixtures.yolokeras import (yolokeras_imageset,
                                yolokeras_equiv_csv_imageset)
from fixtures.sample_query import sample_query
from fixtures.bad_bboxes import query_bad_bboxes


def pytest_addoption(parser):
    parser.addoption("--update-snapshots",
                     action='store_true',
                     help='Update snapshots for image augmentation tests')


def pytest_generate_tests(metafunc):

    update_snapshots = metafunc.config.option.update_snapshots
    if 'snapshot' in metafunc.fixturenames and update_snapshots is not None:
        metafunc.parametrize("snapshot", [{
            "update_snapshots": update_snapshots
        }],
                             ids=["snapshot"])
