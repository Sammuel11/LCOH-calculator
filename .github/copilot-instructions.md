# Copilot instructions for HYDRA (calculadora_streamlit)

## Quick summary
- Entry point: `appInicio.py` — a Streamlit UI for hydrogen transport analysis (LCOH, permeability/diffusion losses, Monte Carlo experiments, fracture propagation).
- Key libraries live in `Codigo/` (not a formal package; modules are imported directly as `Codigo.<module>` from the repo root).

## Quick start / development commands ✅
- Recommended (conda):
  - conda create -n hydra python=3.10 -y
  - conda activate hydra
  - conda install -c conda-forge streamlit pandas numpy plotly matplotlib seaborn scipy
  - **Special:** `assimulo` and `sundials` are required for fracture/ODE modules; install with conda-forge: `conda install -c conda-forge assimulo sundials`
- Or with pip (beware of compiled deps): `pip install streamlit pandas numpy plotly matplotlib seaborn scipy plotly-express`
- Run the app (from repo root):
  - `streamlit run appInicio.py`

## Files you should know (what they do) 🔧
- `appInicio.py` — Streamlit UI and session_state management. Use this as primary entry point.
- `Codigo/LCOH.py` — LCOH (levelized cost of hydrogen) calculation and Plotly visualizations. Function: `calcular_costo_hidrogeno(...)` returns a dict.
- `Codigo/Permeabilidadcosto_P_1090.py` — permeability & diffusion loss calculations. Function: `calcular_perdidas(...)` returns a pandas DataFrame; several `graficas_...` returning Plotly figures.
- `Codigo/difusionH2_stress_FD.py` — diffusion + stress finite-difference model; key functions:
  - `esfuerzos(T, Ru, n, dift, p_dict, ro_dict, espesor_dict, e_dict, ...)` → runs simulation and returns nested dict results by tramo/year
  - `graficas_esfuerzos_all(resultados, n_time_curves=3)` → returns a dict mapping `tramo` -> Plotly `Figure`
  - `von_misses(resultados, referencia1=150, referencia2=80, ...)` → returns `(fig, fig2)` Plotly figures
- `Codigo/pore_model_scipy_adsorption.py` — **Elastic regime** pore model (with adsorption); key functions:
  - `poro_ad_model(T, Ru, Co, nu, k_trap, ro_pore, ka, kd, n_max, t_end, n_step, ...)` → runs simulation and returns nested dict by (tramo, gas)/year
  - `graficas_poro_ad_model_multi(resultados, tramo, gas)` → returns Plotly `Figure` with 2x2 subplots (NOT `.show()`)
- `Codigo/propagacion_fracturas.py` — **Plastic regime** pore model (with fracture propagation); key functions:
  - `poro_assi_fract(T, Ru, Co, nu, k_trap, ro_pore, Gc_year, t_end, n_step, ...)` → runs DAE simulation and returns nested dict by (tramo, gas)/year
  - `graficas_poro_assi_model_multi(resultados, tramo, gas)` → returns Plotly `Figure` with 2x2 subplots (NOT `.show()`)
- `Codigo/montecarlo*.py`, `fractura_montecarlo.py` — Monte Carlo and fracture propagation experiments, using `assimulo` / `scipy`.
- `Codigo/utils.py` — helper for applying CSS and Plotly formatting (`local_css`, `aplicarFormatoChart`).
- Data / assets: `tramos.csv` (note: uses `;` separator), `planimetria.png`, CSS in `Codigo/estilos.css` and `pruebas/estilos.css`.

## Project-specific conventions and gotchas ⚠️
- Working directory matters: run commands from the project root so imports like `Codigo.LCOH` resolve correctly.
- Files use Spanish identifiers and comments. Keep names and units consistent (temperature = K, pressure in Pa, lengths in m, LCOH in USD/kg or USD/L).
- Plotting functions return Plotly figures (do not call `.show()` inside library functions — Streamlit expects figure objects).
- `requerimientos.txt` is currently empty — if you add or change dependencies, update it.
- Heavy/compiled dependencies (`assimulo`, `sundials`) are best installed from `conda-forge`.

## How to run or test small pieces (examples) 💡
- Compute default LCOH from a shell (repo root):
  - `python -c "from Codigo.LCOH import calcular_costo_hidrogeno; print(calcular_costo_hidrogeno())"`
- Compute losses example:
  - `python -c "from Codigo.Permeabilidadcosto_P_1090 import calcular_perdidas; import Codigo.LCOH as L; print(calcular_perdidas(T=298.15, presiones=[1.4e5], gases={'H2':{'Perm':6.153e-16,'Dif':1.213e-10}}, tamanos_rde_11=[{'RDE':'RDE 11','Diametro':25e-3,'espesor':3e-3}], costo_hidrogeno=0.001, longitudes={'H2':1000}))"`
- Run diffusion/stress simulation from Python (CLI):
  - `python -c "import Codigo.difusionH2_stress_FD as d; res = d.esfuerzos(); figs = d.graficas_esfuerzos_all(res); print(list(figs.keys()))"`
- Run pore elastic regime from Python (CLI):
  - `python -c "import Codigo.pore_model_scipy_adsorption as p; res = p.poro_ad_model(); fig = p.graficas_poro_ad_model_multi(res, 'Tramo producción', 'H2'); print('Done')"`
- Run pore plastic regime from Python (CLI):
  - `python -c "import Codigo.propagacion_fracturas as p; res = p.poro_assi_fract(); fig = p.graficas_poro_assi_model_multi(res, 'Tramo producción', 'H2'); print('Done')"`
- Or use the app UI: open streamlit and go to desired menu. Results are cached in `st.session_state` by menu name.

## Good edits for AI / PRs (what to preserve & improve) ✍️
- Preserve Spanish variable names and inline domain units in code (they encode domain knowledge).
- Add a populated `requerimientos.txt` or `environment.yml` (conda) when adding packages.
- Prefer returning data structures (dict / DataFrame / Plotly fig) from library functions — the code already follows this pattern.
- Add a small `tests/` folder with smoke tests for `LCOH.calcular_costo_hidrogeno` and `Permeabilidadcosto_P_1090.calcular_perdidas`.
- When changing imports, ensure the code still runs from project root and update usage examples.

## Debugging tips
- Most common errors: missing package (install via pip/conda), compiled-dep issues for `assimulo`, or `FileNotFoundError` for `tramos.csv`/`planimetria.png` (run from repo root).
- Use `streamlit run appInicio.py --logger.level=debug` to see Streamlit logs.

---
If any of these items are unclear or you'd like me to add tests, a `requirements` file, or a short CONTRIBUTING note, tell me which you prefer and I'll update the file. ✅
