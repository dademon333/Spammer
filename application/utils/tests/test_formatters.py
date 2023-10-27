import pytest

from application.utils.formatters import normalize_phone


@pytest.mark.parametrize(
    "phone",
    (
        "9123456789",
        "79123456789",
        "+79123456789",
        "89123456789",
        "+7 (912) 345-67-89",
    ),
)
def test_normalize_phone(phone: str):
    assert normalize_phone(phone) == "79123456789"
