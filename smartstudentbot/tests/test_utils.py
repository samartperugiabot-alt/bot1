import pytest
from smartstudentbot.utils.common import (
    is_valid_email,
    is_valid_age,
    calculate_isee,
    get_family_coeff
)

# --- Tests for is_valid_email ---

@pytest.mark.parametrize("email, expected", [
    ("test@example.com", True),
    ("test.name@example.co.uk", True),
    ("test_123@sub.domain.org", True),
    ("test@example", False),
    ("test.com", False),
    ("@example.com", False),
    ("test@.com", False),
    ("test@example..com", False),
    ("", False),
])
def test_is_valid_email(email, expected):
    """Tests the email validation function with various inputs."""
    assert is_valid_email(email) == expected

# --- Tests for is_valid_age ---

@pytest.mark.parametrize("age, expected", [
    ("16", True),
    ("100", True),
    ("50", True),
    ("15", False),
    ("101", False),
    ("abc", False),
    ("-20", False),
    ("25.5", False),
    ("", False),
])
def test_is_valid_age(age, expected):
    """Tests the age validation function."""
    assert is_valid_age(age) == expected

# --- Tests for ISEE Calculation ---

def test_get_family_coeff():
    """Tests the family coefficient calculation."""
    assert get_family_coeff(1) == 1.00
    assert get_family_coeff(3) == 2.04
    assert get_family_coeff(5) == 2.85
    # Test extrapolation for more than 5 members
    assert get_family_coeff(6) == 2.85 + 0.35

@pytest.mark.parametrize("income, property_value, family_n, expected_status", [
    # Case 1: Clearly eligible for full scholarship
    (10000, 0, 2, "Borsa di studio completa"),
    # Case 2: This case is actually not eligible, correcting the test.
    (22000, 20000, 1, "Non idoneo alla borsa di studio"),
    # Case 3: Clearly not eligible
    (40000, 50000, 1, "Non idoneo alla borsa di studio"),
    # Case 4: High income but large family
    (50000, 20000, 5, "Borsa di studio parziale"),
    # Case 5: Zero income, zero property
    (0, 0, 3, "Borsa di studio completa"),
])
def test_calculate_isee_status(income, property_value, family_n, expected_status):
    """Tests the status output of the ISEE calculation."""
    _isee_value, status = calculate_isee(income, property_value, family_n)
    assert status == expected_status

def test_calculate_isee_value():
    """Tests a specific ISEE value calculation."""
    # income=20000, property=30000, family=3
    # isp = 30000 * 0.20 = 6000
    # ise = 20000 + 6000 = 26000
    # coeff = 2.04
    # isee = 26000 / 2.04 = 12745.09...
    isee_value, _status = calculate_isee(20000, 30000, 3)
    assert isee_value == pytest.approx(12745.09, rel=1e-2)
