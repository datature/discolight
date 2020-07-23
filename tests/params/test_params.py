import pytest
from discolight.params.params import Params


def test_params_default_substitution_works():
    def f(a, b):
        assert a == 1
        assert b == 2

    params = Params().add("a", "", int, 1).add("b", "", int, 2)

    params.call_with_params(f, {"a": 1})


def test_missing_required_throws_exception():
    def f(_a):
        pass

    params = Params().add("a", "", int, 0, True)

    with pytest.raises(ValueError):
        params.call_with_params(f, {})


def test_wrong_type_throws_exception():
    def f(_a):
        pass

    params = Params().add("a", "", int, 0)

    with pytest.raises(ValueError):
        params.call_with_params(f, {"a": "hello"})


def test_ensure_conditions_checked():
    def f(_a):
        pass

    params = Params().add("a", "", int,
                          0).ensure(lambda params: params["a"] >= 0, "a >= 0")

    with pytest.raises(ValueError):
        params.call_with_params(f, {"a": -1})


def test_unrecognized_param_throws_exception():
    def f(_a, _b):
        pass

    params = Params().add("a", "", int, 0).add("b", "", int, 0)

    with pytest.raises(ValueError):
        params.call_with_params(f, {"c": 3})


def test_with_bound_type_cast_works():
    def type_cast(_v):
        raise RuntimeError("Should not be called")

    def actual_type_cast(v):
        return int(v)

    def f(a):
        assert a == 1

    params = Params().add("a", "", type_cast, 0)

    params.with_bound_type_cast(type_cast, actual_type_cast).call_with_params(
        f, {"a": "1"})
