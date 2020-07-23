import pytest
from discolight.disco import disco


def test_disco_fails_on_non_existent_augmentation():

    with pytest.raises(AttributeError):
        disco.AAAAA()
