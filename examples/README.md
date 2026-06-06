# Examples

Jupyter notebooks demonstrating `squidink`. These live outside `src/`, so they
are part of the repository but are never packaged into the wheel.

## Notebooks

- [`01_consumption.ipynb`](01_consumption.ipynb) — fetch half-hourly electricity
  consumption for a meter.

## Running them

From the repository root:

```bash
pip install -e . --group examples   # squidink + jupyter + nbstripout + python-dotenv
jupyter lab examples/
```

Credentials are loaded from a local `.env` file. Copy the template and fill in
your own details:

```bash
cp .env.example .env
# then edit .env:
#   OCTOPUS_API_KEY=sk_live_...
#   OCTOPUS_MPAN=...
#   OCTOPUS_METER_SERIAL_NUMBER=...
```

`.env` is gitignored, so your real secrets never get committed. `.env.example`
(committed) just documents the variable names.

## A note on committing notebooks

Notebook output cells can contain your data — and, if you typed it in, your API
key. This repo uses [`nbstripout`](https://github.com/kynan/nbstripout) as a git
filter so output and execution counts are stripped automatically on commit.

After cloning, enable it once:

```bash
nbstripout --install --attributes .gitattributes
```
