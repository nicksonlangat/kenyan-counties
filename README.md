# Kenyan Counties

A lightweight, performant Python package providing data for all 47 counties, constituencies, and wards in Kenya. Optimized for speed with zero I/O overhead at runtime.

## Installation

```bash
# Core only
pip install kenyan-counties

# With FastAPI / Pydantic support
pip install kenyan-counties[fastapi]

# With Django support
pip install kenyan-counties[django]

# Everything
pip install kenyan-counties[all]
```

## Usage

### Core API

```python
from kenyan_counties import (
    get_all_counties,
    get_county_by_code,
    get_county_by_name,
    get_constituencies_for_county,
    get_wards_for_constituency,
)

# All 47 counties
counties = get_all_counties()

# Lookup by code (1-47)
mombasa = get_county_by_code(1)
print(mombasa)  # <County: Mombasa (1)>

# Lookup by name (case-insensitive)
nairobi = get_county_by_name("nairobi")
print(nairobi.code)  # 47

# Constituencies in a county
constituencies = get_constituencies_for_county(1)

# Wards in a constituency
wards = get_wards_for_constituency(1, "Changamwe")
print(wards[0].name)  # Port Reitz
```

### FastAPI

```python
from fastapi import FastAPI
from kenyan_counties.fastapi import router

app = FastAPI()
app.include_router(router)
```

The router exposes ready-to-use endpoints. To add custom logic, import the Pydantic models and core functions directly:

```python
from kenyan_counties.fastapi import CountyModel, ConstituencyModel, WardModel
from kenyan_counties.core import get_county_by_name, get_wards_for_constituency

@app.get("/search", response_model=CountyModel)
def search_county(name: str):
    county = get_county_by_name(name)
    if not county:
        raise HTTPException(status_code=404, detail="County not found")
    return CountyModel(
        code=county.code,
        name=county.name,
        constituencies=[
            ConstituencyModel(
                name=c.name,
                wards=[WardModel(name=w.name) for w in c.wards]
            )
            for c in county.constituencies
        ]
    )
```

This adds the following endpoints:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/counties/` | List all 47 counties |
| GET | `/counties/{code}` | Get a county by code |
| GET | `/counties/{code}/constituencies` | List constituencies for a county |

### Django

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "kenyan_counties",
]
```

Run migrations and seed the database:

```bash
python manage.py migrate
python manage.py load_kenya_counties
```

This creates `County`, `Constituency`, and `Ward` records you can query via the Django ORM.

**Using the models in views or serializers:**

```python
from kenyan_counties.models import County, Constituency, Ward

# In a view
def county_list(request):
    counties = County.objects.all()
    ...

# In a DRF serializer
class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = ["id", "name"]

class ConstituencySerializer(serializers.ModelSerializer):
    wards = WardSerializer(many=True, read_only=True)

    class Meta:
        model = Constituency
        fields = ["id", "name", "wards"]

class CountySerializer(serializers.ModelSerializer):
    constituencies = ConstituencySerializer(many=True, read_only=True)

    class Meta:
        model = County
        fields = ["code", "name", "constituencies"]
```

## License

MIT
