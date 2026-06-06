# squidink

A Python client for the [Octopus Energy API](https://developer.octopus.energy/).

> **Status:** Early development. The `0.0.x` line is a name-reservation placeholder
> while the public API takes shape. The first usable release will be `0.1.0`.

## Planned features

- Sync and async client (built on [`httpx`](https://www.python-httpx.org/))
- Typed response models (pydantic)
- Flexible credential storage (explicit args, environment variables, or OS keyring)
- REST coverage of accounts, meter points, consumption, products, and tariffs
- GraphQL support for Intelligent Octopus dispatch data and live smart meter
  telemetry (later)

## Installation

```bash
pip install squidink
```

(Once `0.1.0` is published — the current `0.0.x` releases are placeholders.)

## License

[MIT](LICENSE)
