> **Idiomas:** 🇺🇸 [English](README.md) | 🇪🇸 [Español](README.es.md)
---

# HYDRA: Levelized Cost of Hydrogen Calculator

A Streamlit web application for estimating the levelized cost of hydrogen (LCOH) for an electrolysis project. Users can change technical and economic inputs, calculate costs under those assumptions, and review how the main cost components contribute to the result.

## Current scope

The application in `appInicio.py` has two sections:

- **Home:** introduces the calculator, its assumptions and limitations, and a research reference on green hydrogen costs.
- **LCOH calculation:** provides the input form and displays the LCOH in USD/kg, with charts showing the shares of CAPEX, OPEX, and replacement costs.

This version does not include diffusion, pipeline analysis, fracture, Monte Carlo, or the other modules described in earlier documentation.

## Requirements

- Python 3.10 or later.
- The application's direct dependencies are Streamlit and Plotly.
- Run commands from the project root, where `appInicio.py` and `Codigo\LCOH.py` are located.

## Installation and launch on Windows

In PowerShell, from the project root:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install streamlit==1.47.0 plotly==5.24.1
python -m streamlit run appInicio.py
```

The application is usually available at `http://localhost:8501`. If the `py` command is not available, use `python` to create the virtual environment. If PowerShell blocks environment activation, you can skip activation and run:

```powershell
.\.venv\Scripts\python.exe -m pip install streamlit==1.47.0 plotly==5.24.1
.\.venv\Scripts\python.exe -m streamlit run appInicio.py
```

Running Streamlit with `python -m streamlit` helps ensure that it uses the same Python interpreter where the dependencies were installed.

## Using the application

1. Open **LCOH calculation** from the sidebar or the button on the Home page.
2. Set the technical and economic parameters in the form.
3. Select **Calculate LCOH** to update the estimate.
4. Review the result in USD/kg and the cost distribution charts.

The application stores the latest calculated result in Streamlit's session state.

## Input parameters

The following table shows the form's initial values:

| Group | Parameter | Model variable | Initial value | Unit |
|---|---|---:|---:|---|
| CAPEX | Electrolyzer power | `p_el` | 1,000 | kW |
| CAPEX | Electrolyzer cost | `costo_el` | 1,345 | USD/kW |
| CAPEX | Engineering factor | `a` | 0.19 | Share of direct cost |
| CAPEX | Licensing factor | `b` | 0.01 | Share of direct cost |
| CAPEX | Contingency factor | `c` | 0.15 | Share of direct cost |
| OPEX | Electrolysis efficiency | `efic_el` | 0.65 | Share |
| OPEX | Electricity cost (LCOE) | `LCOE` | 0.053 | USD/kWh |
| OPEX | Water consumption | `consumo_agua` | 15 | L/kg H₂ |
| OPEX | Water price | `precio_agua` | 0.006 | USD/L |
| OPEX | Maintenance factor | `psi` | 0.05 | Share of direct cost |
| Replacement | Replacement cost factor | `d` | 0.4 | Share of direct cost |
| Replacement | Replacement year | `t` | 7 | Years |
| Production | Electrolyzer specific energy consumption | `PC` | 54 | kWh/kg H₂ |
| Production | Operating hours per year | `ha` | 8,760 | h/year |
| Finance | Discount rate | `tasa_descuento` | 0.08 | Share |
| Finance | Project lifetime | `vida_proyecto` | 20 | Years |

The form limits power to 100,000 kW and annual operating hours to 8,760. Efficiency and the discount rate accept values from 0 to 1. To keep the calculation finite, do not set power, efficiency, specific energy consumption, or the discount rate to zero.

The `PC` field is labeled `kW/kg` in the interface. The model and its documentation treat it as specific energy consumption in `kWh/kg H₂`.

## Implemented calculation method

The model calculates annual hydrogen production as follows:

```text
Annual production (kg H₂) = annual hours × power × efficiency / specific energy consumption
```

Direct capital cost is calculated by multiplying electrolyzer power by its specific cost. Engineering, licensing, and contingencies are calculated as shares of this direct cost. CAPEX is annualized with the capital recovery factor:

```text
CRF = i × (1 + i)^N / ((1 + i)^N − 1)
Annualized CAPEX = (direct cost + engineering + licensing + contingencies) × CRF
```

Annual OPEX is the sum of electricity, water, and maintenance costs. Replacement cost is discounted from the year entered in the form and annualized using the same capital recovery factor. Finally:

```text
LCOH (USD/kg) = (annualized CAPEX + annual OPEX + annualized replacement cost)
                / annual hydrogen production
```

In `Codigo\LCOH.py`, the `calcular_costo_hidrogeno(...)` function also returns an LCOH value in USD/L and cost and production data. The current interface displays the USD/kg value and USD/kg charts; it does not display the USD/L value.

### Charts and results

- Total cost in USD/kg.
- Stacked bar chart showing the CAPEX, OPEX, and replacement contributions to the LCOH.
- Pie chart showing the percentage distribution of those components.

## Assumptions and limitations

- The model calculates a deterministic scenario using the values entered in the form.
- It assumes continuous, stable plant operation and constant hydrogen demand.
- It does not model gradual electrolyzer degradation or interruptions in the electricity supply.
- It does not include tax incentives, tax deductions, taxes, or import tariffs.
- It does not include sensitivity analysis, Monte Carlo simulations, or optimization.
- The calculation function retains a `fu` parameter, but the form does not expose it and the implemented equations do not use it.
- Results depend on the input data and do not replace a project-specific financial or engineering assessment.

## Research reference shown on the Home page

Benalcazar, P. and Komorowska, A. (2024). “Techno-economic analysis and uncertainty assessment of green hydrogen production in future exporting countries”. *Renewable and Sustainable Energy Reviews*, 199, 114512.

For Colombia, the paper reports an LCOH of USD 4.1–4.9/kg by 2030 in the scenarios it analyzes. This range is a reference from that study, not a universal range or a prediction produced by this calculator. The differences in scope and assumptions should be considered before comparing results.

## Relevant project structure

```text
.
├── appInicio.py       # Streamlit interface: Home and LCOH calculation
├── requerimientos.txt # Project dependency list
└── Codigo
    └── LCOH.py        # LCOH calculation function and charts
```

## Basic checks

From the project root, check the Python syntax:

```powershell
python -m py_compile appInicio.py Codigo\LCOH.py
```

Check that the calculation and chart functions can be imported and run:

```powershell
python -c "from Codigo.LCOH import calcular_costo_hidrogeno, grafico_lcoh, grafico_lcoh_pie; r = calcular_costo_hidrogeno(); print('LCOH: {:.2f} USD/kg'.format(r['LCOH_kg'])); grafico_lcoh(r); grafico_lcoh_pie(r)"
```

## Troubleshooting

### `streamlit` is not recognized or returns `command not found`

Run Streamlit with the active Python interpreter:

```powershell
python -m streamlit run appInicio.py
```

### `ModuleNotFoundError: No module named 'plotly'` or `streamlit`

Install the packages with the same interpreter you will use to launch the application:

```powershell
python -m pip install plotly==5.24.1 streamlit==1.47.0
python -m streamlit run appInicio.py
```

### `ModuleNotFoundError: No module named 'Codigo'`

Run the command from the project root and check that `Codigo\LCOH.py` exists.
