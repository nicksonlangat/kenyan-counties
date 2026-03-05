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

## License

MIT
