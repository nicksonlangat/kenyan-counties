# Design Decisions

## Django vs FastAPI Integration Philosophy

### Why Django touches the database

Django ships with its own ORM built in. When someone installs a Django app, they expect it to have models and migrations. The whole point of the Django integration is to give you real database records you can query, filter, join, and manage via the admin panel — that is the Django way.

So the package ships:
- `models.py` — County, Constituency, Ward as Django ORM models
- `migrations/` — so tables are created automatically on `migrate`
- `management/commands/load_kenya_counties.py` — seeds the database from the built-in data
- `admin.py` — registers all models in Django admin out of the box

### Why FastAPI does not touch the database

FastAPI is intentionally database-agnostic. It does not care whether you use SQLAlchemy, Tortoise ORM, Beanie, Prisma, or no database at all. Shipping SQLAlchemy models would:

- Force a database dependency on users who may not want one
- Pick a specific ORM when the user may already use a different one
- Add unnecessary complexity for a problem that does not require a database

The data in this package is static — 47 counties, their constituencies and wards do not change at runtime. So the FastAPI integration serves data directly from an in-memory Python dictionary (`data.py`) via Pydantic models. This is faster than a database query, requires zero setup, and works with any FastAPI project regardless of their stack.

If a FastAPI user needs the data in their own database (e.g. to join against their own models), they can use the core API to seed it with whatever ORM they use:

```python
from kenyan_counties import get_all_counties

counties = get_all_counties()
# seed into your own DB however you like
```

### Summary

| | Django | FastAPI |
|---|---|---|
| Data source | Your database (SQLite, Postgres, etc.) | In-memory dict |
| Why | ORM is standard; DB records are queryable, joinable, and admin-able | Framework is DB-agnostic; static data needs no database |
| Setup | `migrate` + `load_kenya_counties` | None |
| Trade-off | Requires DB setup | No DB-level querying out of the box |

The rule of thumb: integrate deeply with the framework's conventions, but never impose opinions that belong to the user's stack.
