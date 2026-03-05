import pytest
from kenyan_counties.fastapi import CountyModel, ConstituencyModel, WardModel
from kenyan_counties.core import get_county_by_code
from pydantic import ValidationError

def test_pydantic_models():
    # Fetch a county dictionary essentially
    county = get_county_by_code(1)
    
    # Can we convert our core models to dictionaries that Pydantic understands?
    # Or directly from the original JSON dict? Since we already transformed them
    # into objects in `core.py`, let's serialize them to dicts first for the test
    
    # We can reconstruct it to dict easily for the test
    county_dict = {
        "code": county.code,
        "name": county.name,
        "constituencies": [
            {
                "name": c.name,
                "wards": [{"name": w.name} for w in c.wards]
            }
            for c in county.constituencies
        ]
    }
    
    # Try parsing
    model = CountyModel(**county_dict)
    
    assert model.code == 1
    assert model.name == "Mombasa"
    assert len(model.constituencies) == 6
    assert isinstance(model.constituencies[0], ConstituencyModel)
    assert isinstance(model.constituencies[0].wards[0], WardModel)
    
def test_pydantic_validation_error():
    with pytest.raises(ValidationError):
        # Missing required 'code' and 'name'
        CountyModel(something_else="Invalid")
