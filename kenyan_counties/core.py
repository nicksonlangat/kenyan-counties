from typing import List, Optional

from .data import KENYA_COUNTIES_DATA

class Ward:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<Ward: {self.name}>"

class Constituency:
    def __init__(self, name: str, wards: List[str]):
        self.name = name
        self.wards = [Ward(w) for w in wards]

    def __repr__(self):
        return f"<Constituency: {self.name}>"

class County:
    def __init__(self, code: int, name: str, constituencies: List[dict]):
        self.code = code
        self.name = name
        self.constituencies = [
            Constituency(c["constituency_name"], c["wards"]) for c in constituencies
        ]

    def __repr__(self):
        return f"<County: {self.name} ({self.code})>"

# Pre-compute data structures for fast O(1) lookups
_ALL_COUNTIES = [
    County(c["county_code"], c["county_name"], c["constituencies"])
    for c in KENYA_COUNTIES_DATA
]

_COUNTY_BY_CODE = {c.code: c for c in _ALL_COUNTIES}
_COUNTY_BY_NAME = {c.name.lower(): c for c in _ALL_COUNTIES}


def get_all_counties() -> List[County]:
    """Returns a list of all 47 counties."""
    return _ALL_COUNTIES


def get_county_by_code(code: int) -> Optional[County]:
    """Returns a County object by its integer code (1-47)."""
    return _COUNTY_BY_CODE.get(code)


def get_county_by_name(name: str) -> Optional[County]:
    """Returns a County object by its string name (case-insensitive)."""
    return _COUNTY_BY_NAME.get(name.lower())


def get_constituencies_for_county(county_code: int) -> List[Constituency]:
    """Returns a list of Constituency objects for a given county code."""
    county = get_county_by_code(county_code)
    if county:
        return county.constituencies
    return []


def get_wards_for_constituency(county_code: int, constituency_name: str) -> List[Ward]:
    """Returns a list of Ward objects for a given county code and constituency name."""
    county = get_county_by_code(county_code)
    if not county:
        return []

    target_name = constituency_name.lower().strip()
    for const in county.constituencies:
        if const.name.lower().strip() == target_name:
            return const.wards
    
    return []
