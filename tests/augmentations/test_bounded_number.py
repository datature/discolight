import pytest
from discolight.augmentations.augmentation.types import BoundedNumber


def test_bounded_number_coerces_to_number_type():

    f = BoundedNumber(float)

    num = f(3)

    assert type(num) == float
    assert num == 3.0

    num = f(3.0)

    assert type(num) == float
    assert num == 3.0

    i = BoundedNumber(int)

    num = i(3)

    assert type(num) == int
    assert num == 3

    num = i(3.0)

    assert type(num) == int
    assert num == 3


def test_bounded_number_minimum():

    n = BoundedNumber(float, 1.0)

    n(1.0)
    n(1)
    n(1.1)

    with pytest.raises(ValueError):
        n(0.9)
        n(-1)


def test_bounded_number_maximum():

    n = BoundedNumber(float, maximum=1.0)

    n(0.9)
    n(1.0)
    n(1)
    n(-1)

    with pytest.raises(ValueError):
        n(1.1)

    with pytest.raises(ValueError):
        n(5)


def test_bounded_number_minimum_and_maximum():

    n = BoundedNumber(float, 1.0, 2.0)

    n(1.1)
    n(1.0)
    n(2.0)
    n(1)
    n(2)

    with pytest.raises(ValueError):
        n(3)
    with pytest.raises(ValueError):
        n(-1)
    with pytest.raises(ValueError):
        n(2.5)
    with pytest.raises(ValueError):
        n(0.9)
