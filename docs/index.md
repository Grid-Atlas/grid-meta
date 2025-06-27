# Getting Started with `grid-meta`

[![Build](https://github.com/Grid-Atlas/grid-meta/actions/workflows/ci.yml/badge.svg)](https://github.com/Grid-Atlas/grid-meta/actions/workflows/ci.yml)
![Python](https://img.shields.io/pypi/pyversions/grid-meta)
![License](https://img.shields.io/github/license/Grid-Atlas/grid-meta)
![Coverage](https://img.shields.io/codecov/c/github/Grid-Atlas/grid-meta)

[View Full Documentation.](https://grid-atlas.github.io/grid-meta).

Welcome! Follow the steps below to get `grid-meta` up and running locally.  
We recommend using a Python virtual environment for a clean install 🔒🐍.

> 💡 **Note:** In the future, `grid-meta` may be installable directly via `pip install gridmeta`. For now, follow the instructions below.

---

## 📦 Step 1: Clone the Repository

First, download the codebase to your machine:

```bash
git clone https://github.com/Grid-Atlas/grid-meta.git
cd grid-meta
```

## 🧪 Step 2: Set Up a Python Environment

To avoid dependency conflicts, create and activate a virtual environment.

You can use any tool of your choice — here are a few popular options:

<details> <summary><strong>🟢 Option A: Using <code>venv</code> (Standard Library)</strong></summary>

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

</details> <details> <summary><strong>🔵 Option B: Using <code>conda</code></strong></summary>

```bash
conda create -n grid-reducer-env python=3.10
conda activate grid-reducer-env
```

</details>

## 🚀 Step 3: Install the Project Locally

Install the project in editable mode so changes to the code reflect immediately:

```bash
pip install -e .
```

✅ This will also install all required dependencies.

## 🛠 Example CLI Usage

You can currently use this package as CLI tool. To see the available commands please use following command.

```bash
gridmeta --help
```

```bash
Usage: gridmeta [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  extract-opendss-dehydrated-dataset
```

To extract opendss model dehydrated metadata you can use following command.

```bash
gridmeta extract-opendss-dehydrated-dataset -f tests\data\opendss\ieee13\master.dss -o test.json
```

You can specify privacy flag with `-pm` option.

```bash
gridmeta extract-opendss-dehydrated-dataset -f tests\data\opendss\ieee13\master.dss -pm "low" -o test.json
```

Make sure to pass appropriate file paths. You can also update model year, state, region type and description from command line.
Defaults will be used if these are not provided.

## Example

Here is an example of extracted metadata for IEEE 13 opendss model.

```json
{
  "metadata": {
    "state": "WA",
    "created_at": "2025-02-26T16:07:47.810263",
    "model_year": 2025,
    "info": "",
    "region_type": "Suburban"
  },
  "assets": {
    "transformers": [
      {
        "kva": 500,
        "count": 1,
        "is_regulator": false,
        "is_substation_transformer": false,
        "num_phase": 3,
        "high_kv": 4.16,
        "low_kv": 0.48,
        "avg_customers_served": 3.0,
        "min_customers_served": 3.0,
        "max_customers_served": 3.0,
        "std_customers_served": "NaN",
        "min_pct_peak_loading": 107.2857856604396,
        "avg_pct_peak_loading": 107.2857856604396,
        "max_pct_peak_loading": 107.2857856604396,
        "std_pct_peak_loading": "NaN"
      },
      {
        "kva": 1666,
        "count": 3,
        "is_regulator": true,
        "is_substation_transformer": false,
        "num_phase": 1,
        "high_kv": 2.4,
        "low_kv": 2.4,
        "avg_customers_served": 5.0,
        "min_customers_served": 0.0,
        "max_customers_served": 15.0,
        "std_customers_served": 8.660254037844387,
        "min_pct_peak_loading": 56.934951911321086,
        "avg_pct_peak_loading": 72.20336662873115,
        "max_pct_peak_loading": 81.85450680902247,
        "std_pct_peak_loading": 13.375776014643415
      },
      {
        "kva": 5000,
        "count": 1,
        "is_regulator": false,
        "is_substation_transformer": true,
        "num_phase": 3,
        "high_kv": 115.0,
        "low_kv": 4.16,
        "avg_customers_served": 15.0,
        "min_customers_served": 15.0,
        "max_customers_served": 15.0,
        "std_customers_served": "NaN",
        "min_pct_peak_loading": 80.6972565800457,
        "avg_pct_peak_loading": 80.6972565800457,
        "max_pct_peak_loading": 80.6972565800457,
        "std_pct_peak_loading": "NaN"
      }
    ],
    "feeder_sections": [
      {
        "kv": 2.40178,
        "num_phase": 1.0,
        "count": 2.0,
        "avg_feeder_miles": 0.16763999999999998,
        "min_feeder_miles": 0.09144,
        "max_feeder_miles": 0.24383999999999997,
        "std_feeder_miles": 0.10776307345282983,
        "min_ampacity": 400.0,
        "avg_ampacity": 400.0,
        "max_ampacity": 400.0,
        "std_ampacity": 0.0,
        "avg_per_unit_resistance_ohm_per_mile": 8.259058763487898e-5,
        "min_per_unit_resistance_ohm_per_mile": 4.504941143720672e-5,
        "max_per_unit_resistance_ohm_per_mile": 0.00012013176383255125,
        "std_per_unit_resistance_ohm_per_mile": 5.309124052618614e-5,
        "avg_per_unit_reactance_ohm_per_mile": 0.00017173146325459316,
        "min_per_unit_reactance_ohm_per_mile": 9.36717072297781e-5,
        "max_per_unit_reactance_ohm_per_mile": 0.00024979121927940824,
        "std_per_unit_reactance_ohm_per_mile": 0.00011039316564582839,
        "min_customers_served": 1.0,
        "avg_customers_served": 1.0,
        "max_customers_served": 1.0,
        "std_customers_served": 0.0,
        "min_pct_peak_loading": 15.674269355370459,
        "avg_pct_peak_loading": 16.73120979790217,
        "max_pct_peak_loading": 17.788150240433882,
        "std_pct_peak_loading": 1.4947395084489676
      },
      {
        "kv": 2.40178,
        "num_phase": 2.0,
        "count": 3.0,
        "avg_feeder_miles": 0.11175999999999998,
        "min_feeder_miles": 0.09144,
        "max_feeder_miles": 0.15239999999999998,
        "std_feeder_miles": 0.035195272409799576,
        "min_ampacity": 400.0,
        "avg_ampacity": 400.0,
        "max_ampacity": 400.0,
        "std_ampacity": 0.0,
        "avg_per_unit_resistance_ohm_per_mile": 0.0003202409042304056,
        "min_per_unit_resistance_ohm_per_mile": 0.0002217052413902808,
        "max_per_unit_resistance_ohm_per_mile": 0.000369508735650468,
        "std_per_unit_resistance_ohm_per_mile": 8.533438719828638e-5,
        "avg_per_unit_reactance_ohm_per_mile": 0.0007264657732177418,
        "min_per_unit_reactance_ohm_per_mile": 0.0005029378429968982,
        "max_per_unit_reactance_ohm_per_mile": 0.0008382297383281636,
        "std_per_unit_reactance_ohm_per_mile": 0.00019358086602660592,
        "min_customers_served": 1.0,
        "avg_customers_served": 1.6666666666666667,
        "max_customers_served": 2.0,
        "std_customers_served": 0.5773502691896257,
        "min_pct_peak_loading": 16.094312794909246,
        "avg_pct_peak_loading": 23.23659848839567,
        "max_pct_peak_loading": 35.82733535181359,
        "std_pct_peak_loading": 10.936738998493551
      },
      {
        "kv": 2.40178,
        "num_phase": 3.0,
        "count": 6.0,
        "avg_feeder_miles": 0.30479999999999996,
        "min_feeder_miles": 0.15239999999999998,
        "max_feeder_miles": 0.6095999999999999,
        "std_feeder_miles": 0.1788621873986338,
        "min_ampacity": 400.0,
        "avg_ampacity": 400.0,
        "max_ampacity": 400.0,
        "std_ampacity": 0.0,
        "avg_per_unit_resistance_ohm_per_mile": 0.0001431742504224452,
        "min_per_unit_resistance_ohm_per_mile": 5.54263103475702e-5,
        "max_per_unit_resistance_ohm_per_mile": 0.0002217052413902808,
        "std_per_unit_resistance_ohm_per_mile": 7.100745688573208e-5,
        "avg_per_unit_reactance_ohm_per_mile": 0.00032479046606481823,
        "min_per_unit_reactance_ohm_per_mile": 0.00012573446074922454,
        "max_per_unit_reactance_ohm_per_mile": 0.0005029378429968982,
        "std_per_unit_reactance_ohm_per_mile": 0.00016108025673573865,
        "min_customers_served": 0.0,
        "avg_customers_served": 6.333333333333333,
        "max_customers_served": 15.0,
        "std_customers_served": 5.501514942874069,
        "min_pct_peak_loading": 0.00014937875249263795,
        "avg_pct_peak_loading": 76.50571677687857,
        "max_pct_peak_loading": 147.9353947021755,
        "std_pct_peak_loading": 60.66546205074211
      }
    ],
    "capacitors": [
      { "kvar": 100.0, "num_phase": 1.0, "kv": 2.4, "count": 1.0 },
      { "kvar": 600.0, "num_phase": 3.0, "kv": 4.16, "count": 1.0 }
    ],
    "switches": [
      {
        "num_phase": 3.0,
        "kv": 2.40178,
        "is_normally_open": false,
        "count": 1.0,
        "avg_ampacity": 400.0,
        "min_ampacity": 400.0,
        "max_ampacity": 400.0,
        "std_ampacity": "NaN"
      }
    ],
    "loads": [
      {
        "kv": 0.277,
        "count": 3.0,
        "num_phase": 1.0,
        "total_customer": 3.0,
        "avg_customers_per_load": 1.0,
        "min_customers_per_load": 1.0,
        "max_customers_per_load": 1.0,
        "std_customers_per_load": 0.0,
        "avg_peak_kw": 133.33333333333334,
        "avg_peak_kvar": 96.66666666666667,
        "min_peak_kw": 120.0,
        "min_peak_kvar": 90.0,
        "max_peak_kw": 160.0,
        "max_peak_kvar": 110.0,
        "std_peak_kw": 23.094010767585033,
        "std_peak_kvar": 11.547005383792516
      },
      {
        "kv": 2.4,
        "count": 9.0,
        "num_phase": 1.0,
        "total_customer": 9.0,
        "avg_customers_per_load": 1.0,
        "min_customers_per_load": 1.0,
        "max_customers_per_load": 1.0,
        "std_customers_per_load": 0.0,
        "avg_peak_kw": 167.88888888888889,
        "avg_peak_kvar": 96.55555555555556,
        "min_peak_kw": 17.0,
        "min_peak_kvar": 10.0,
        "max_peak_kw": 485.0,
        "max_peak_kvar": 212.0,
        "std_peak_kw": 142.64768175862903,
        "std_peak_kvar": 67.38529348290899
      },
      {
        "kv": 4.16,
        "count": 2.0,
        "num_phase": 1.0,
        "total_customer": 2.0,
        "avg_customers_per_load": 1.0,
        "min_customers_per_load": 1.0,
        "max_customers_per_load": 1.0,
        "std_customers_per_load": 0.0,
        "avg_peak_kw": 200.0,
        "avg_peak_kvar": 141.5,
        "min_peak_kw": 170.0,
        "min_peak_kvar": 132.0,
        "max_peak_kw": 230.0,
        "max_peak_kvar": 151.0,
        "std_peak_kw": 42.42640687119285,
        "std_peak_kvar": 13.435028842544403
      },
      {
        "kv": 4.16,
        "count": 1.0,
        "num_phase": 3.0,
        "total_customer": 1.0,
        "avg_customers_per_load": 1.0,
        "min_customers_per_load": 1.0,
        "max_customers_per_load": 1.0,
        "std_customers_per_load": "NaN",
        "avg_peak_kw": 1155.0,
        "avg_peak_kvar": 660.0,
        "min_peak_kw": 1155.0,
        "min_peak_kvar": 660.0,
        "max_peak_kw": 1155.0,
        "max_peak_kvar": 660.0,
        "std_peak_kw": "NaN",
        "std_peak_kvar": "NaN"
      }
    ]
  },
  "voltage_metrics": [
    {
      "snapshot_category": "NetPeakLoad",
      "kv": 0.27713,
      "num_phase": 3.0,
      "avg_voltage_pu": 0.9926781594690027,
      "min_voltage_pu": 0.9824563162208678,
      "max_voltage_pu": 1.0084186207663994,
      "std_voltage_pu": 0.013832992200133702
    },
    {
      "snapshot_category": "NetPeakLoad",
      "kv": 2.40178,
      "num_phase": 1.0,
      "avg_voltage_pu": 0.968088461668005,
      "min_voltage_pu": 0.9608430966208247,
      "max_voltage_pu": 0.9753338267151852,
      "std_voltage_pu": 0.01024649351406627
    },
    {
      "snapshot_category": "NetPeakLoad",
      "kv": 2.40178,
      "num_phase": 2.0,
      "avg_voltage_pu": 0.9973335665813833,
      "min_voltage_pu": 0.9628590008697668,
      "max_voltage_pu": 1.0197285920694914,
      "std_voltage_pu": 0.022007077364035624
    },
    {
      "snapshot_category": "NetPeakLoad",
      "kv": 2.40178,
      "num_phase": 3.0,
      "avg_voltage_pu": 1.0077043602060967,
      "min_voltage_pu": 0.9629552840078276,
      "max_voltage_pu": 1.0560497133305953,
      "std_voltage_pu": 0.029312299320140376
    },
    {
      "snapshot_category": "NetPeakLoad",
      "kv": 66.39528,
      "num_phase": 3.0,
      "avg_voltage_pu": 0.9999724980882166,
      "min_voltage_pu": 0.9999501168596413,
      "max_voltage_pu": 0.9999938117414283,
      "std_voltage_pu": 2.1866994797273813e-5
    }
  ]
}

```
