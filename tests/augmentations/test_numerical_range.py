import pytest

from discolight.augmentations.augmentation.types import NumericalRange


def test_numerical_range_passthrough():

    r = NumericalRange()

    floor, ceil = r((2.0, 3.0))

    assert floor == 2.0
    assert ceil == 3.0


def test_numerical_range_converts_list():

    r = NumericalRange()

    num_range = r([2.0, 3.0])

    assert type(num_range) == tuple

    assert num_range[0] == 2.0
    assert num_range[1] == 3.0


def test_numerical_range_converts_to_float():

    r = NumericalRange()

    floor, ceil = r([2, 3])

    assert type(floor) == float
    assert type(floor) == float

    assert floor == 2.0
    assert ceil == 3.0


def test_numerical_range_throws_exception_when_max_g_min():

    r = NumericalRange()

    with pytest.raises(ValueError):
        r((3, 2))


def test_numerical_range_global_minimum():

    r = NumericalRange(minimum=0.0)

    r((0.0, 1.0))

    with pytest.raises(ValueError):
        r((-0.1, 1))


def test_numerical_range_global_maximum():

    r = NumericalRange(maximum=1.0)

    r((0.0, 1.0))

    with pytest.raises(ValueError):
        r((0.0, 1.1))


def test_numerical_range_global_max_and_min():

    r = NumericalRange(minimum=0.0, maximum=1.0)

    r((0.0, 1.0))
    r((0.5, 0.6))

    with pytest.raises(ValueError):
        r((-0.1, 0.5))
        r((-0.1, 1.1))
        r((0.1, 1.2))
        r((1.5, 1.7))
        r((-0.5, -0.1))


def test_numerical_range_no_tuple():

    r = NumericalRange()

    with pytest.raises(ValueError):

        r(None)


def test_numerical_range_no_2tuple():

    r = NumericalRange()

    with pytest.raises(ValueError):

        r((1, 2, 3))
