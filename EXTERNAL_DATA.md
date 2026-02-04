# External Reference Data (Encyclopedia, Church Fathers, Summa)

The app can use extra reference data from a sibling folder to enhance study:

- **Catholic Encyclopedia** (cathen) – New Advent
- **Church Fathers** (fathers) – full works with Bible links
- **Summa Theologica** (summa) – St. Thomas Aquinas
- **Douay-Rheims** (douay) and **Library** (library) – when present

## Data location

Point the app at the folder that contains `cathen/`, `fathers/`, `summa/`, etc.

**Default:** `../bible-commentary/data` (sibling project’s `data` folder).

**Override:** set the `EXTERNAL_DATA_ROOT` environment variable:

```bash
set EXTERNAL_DATA_ROOT=C:\Users\...\bible-commentary\bible-commentary\data
```

Or in `.env`:

```
EXTERNAL_DATA_ROOT=C:\Users\...\bible-commentary\bible-commentary\data
```

## API endpoints

- `GET /api/sources/availability` – which collections are available
- `GET /api/sources/{collection}` – list entries (optional `?prefix=`)
- `GET /api/sources/{collection}/search?q=...` – search titles
- `GET /api/sources/{collection}/article/{id}` – full article (e.g. `00001a.htm`)

Collections: `cathen`, `fathers`, `summa`, `douay`, `library`.

## In-app use

- The **curated** Church Fathers quotes in `data/church_fathers_quotes.json` are still used for daily reading and interconnections.
- The **external** `fathers/` and `cathen/` HTM files are available via the API for browsing and search (e.g. a future “Sources” or “Encyclopedia” panel).
