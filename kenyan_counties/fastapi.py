from typing import List, Optional

try:
    from pydantic import BaseModel, Field
except ImportError:
    raise ImportError(
        "pydantic is required for FastAPI integration. "
        "Install it with: pip install kenyan-counties[fastapi]"
    )

try:
    from fastapi import APIRouter, HTTPException
    _has_fastapi = True
except ImportError:
    _has_fastapi = False

from .core import (
    get_all_counties,
    get_county_by_code,
    get_county_by_name,
    get_constituencies_for_county,
    get_wards_for_constituency,
)


class WardModel(BaseModel):
    name: str = Field(..., description="Name of the ward")


class ConstituencyModel(BaseModel):
    name: str = Field(..., description="Name of the constituency")
    wards: List[WardModel] = Field(default_factory=list, description="List of wards in this constituency")


class CountyModel(BaseModel):
    code: int = Field(..., description="Unique county code (1-47)")
    name: str = Field(..., description="Name of the county")
    constituencies: List[ConstituencyModel] = Field(default_factory=list, description="List of constituencies in this county")


def _county_to_model(county) -> CountyModel:
    return CountyModel(
        code=county.code,
        name=county.name,
        constituencies=[
            ConstituencyModel(
                name=c.name,
                wards=[WardModel(name=w.name) for w in c.wards],
            )
            for c in county.constituencies
        ],
    )


if _has_fastapi:
    router = APIRouter(prefix="/counties", tags=["counties"])

    @router.get("/", response_model=List[CountyModel])
    def list_counties():
        """Return all 47 Kenyan counties."""
        return [_county_to_model(c) for c in get_all_counties()]

    @router.get("/{code}", response_model=CountyModel)
    def get_county(code: int):
        """Return a county by its code (1-47)."""
        county = get_county_by_code(code)
        if not county:
            raise HTTPException(status_code=404, detail=f"County with code {code} not found")
        return _county_to_model(county)

    @router.get("/{code}/constituencies", response_model=List[ConstituencyModel])
    def list_constituencies(code: int):
        """Return all constituencies for a given county code."""
        county = get_county_by_code(code)
        if not county:
            raise HTTPException(status_code=404, detail=f"County with code {code} not found")
        return [
            ConstituencyModel(
                name=c.name,
                wards=[WardModel(name=w.name) for w in c.wards],
            )
            for c in county.constituencies
        ]
