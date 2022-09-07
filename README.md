# tap-netsuite-sql

`tap-netsuite-sql` is a Singer tap for DasboardReports.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

### Source Authentication and Authorization

- [ ] `Developer TODO:` If your tap requires special access on the source system, or any special authentication requirements, provide those here.

## Usage

You can easily run `tap-netsuite-sql` by itself or in a pipeline using [Meltano](https://meltano.com/).


### Initialize your Development Environment

```bash
pip install poetry
poetry install
```

### Executing the Tap Directly

```bash
poetry run tap-netsuite-sql --config ./config.json
```
