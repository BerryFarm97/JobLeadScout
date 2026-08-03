import pytest

from app.formatters import format_salary_range


@pytest.mark.parametrize(
    ("salary_min", "salary_max", "expected"),
    [
        (None, None, "Unknown"),
        (55_000.0, 55_000.0, "$55,000"),
        (55_000.0, None, "From $55,000"),
        (None, 70_000.0, "Up to $70,000"),
        (55_000.0, 70_000.0, "$55,000 - $70,000"),
    ],
)
def test_format_salary_range(salary_min, salary_max, expected):
    assert format_salary_range(salary_min, salary_max) == expected
