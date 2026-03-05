import pytest
from kenyan_counties.core import (
    get_all_counties,
    get_county_by_code,
    get_county_by_name,
    get_constituencies_for_county,
    get_wards_for_constituency,
    County,
    Constituency,
    Ward
)

def test_get_all_counties():
    counties = get_all_counties()
    assert len(counties) == 47
    assert isinstance(counties[0], County)

def test_get_county_by_code():
    mombasa = get_county_by_code(1)
    assert mombasa is not None
    assert mombasa.name == "Mombasa"
    
    invalid = get_county_by_code(99)
    assert invalid is None

def test_get_county_by_name():
    nairobi = get_county_by_name("Nairobi")
    assert nairobi is not None
    assert nairobi.code == 47
    
    # Test case insensitivity
    nairobi_lower = get_county_by_name("nairobi")
    assert nairobi_lower is not None
    assert nairobi_lower.code == 47
    
    invalid = get_county_by_name("Not A County")
    assert invalid is None

def test_get_constituencies_for_county():
    # Mombasa has 6 constituencies
    constituencies = get_constituencies_for_county(1)
    assert len(constituencies) == 6
    assert isinstance(constituencies[0], Constituency)
    
    # Check for invalid county code
    invalid = get_constituencies_for_county(99)
    assert len(invalid) == 0

def test_get_wards_for_constituency():
    # Mombasa -> Changamwe has 5 wards
    wards = get_wards_for_constituency(1, "Changamwe")
    assert len(wards) == 5
    assert isinstance(wards[0], Ward)
    assert wards[0].name == "Port Reitz"
    
    # Test case insensitivity
    wards_lower = get_wards_for_constituency(1, "changamwe")
    assert len(wards_lower) == 5
    
    # Test invalid county code
    invalid_county = get_wards_for_constituency(99, "Changamwe")
    assert len(invalid_county) == 0
    
    # Test invalid constituency
    invalid_const = get_wards_for_constituency(1, "Not A Constituency")
    assert len(invalid_const) == 0
