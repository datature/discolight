from discolight.util.decorators import singleton


@singleton
class A:
    def __init__(self):
        self.a = 0

    def inc(self):
        self.a += 1
        return self.a


def test_singleton():

    assert A().inc() == 1
    assert A().inc() == 2
    assert A().inc() == 3
