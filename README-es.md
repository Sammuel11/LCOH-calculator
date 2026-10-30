# HYDRA: calculadora del costo nivelado de hidrógeno

Aplicación web desarrollada con Streamlit para estimar el costo nivelado de hidrógeno (LCOH) de un proyecto de electrólisis. La interfaz permite modificar parámetros técnicos y económicos, calcular el costo con esos supuestos y consultar la distribución del resultado.

## Alcance actual

La aplicación disponible en `appInicio.py` tiene dos secciones:

- **Inicio:** presenta el propósito de la calculadora, sus supuestos y limitaciones, y una referencia bibliográfica sobre costos de hidrógeno verde.
- **Cálculo del LCOH:** contiene el formulario de parámetros y muestra el LCOH en USD/kg junto con gráficos de la participación del CAPEX, el OPEX y el reemplazo.

Esta versión no incluye los módulos de difusión, análisis de tuberías, fractura, Monte Carlo ni los otros módulos mencionados en documentación anterior.

## Requisitos

- Python 3.10 o superior.
- Las dependencias directas de la aplicación son Streamlit y Plotly.
- Ejecutar los comandos desde la carpeta raíz del proyecto, donde se encuentran `appInicio.py` y `Codigo\LCOH.py`.

## Instalación y ejecución en Windows

En PowerShell, desde la raíz del proyecto:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install streamlit==1.47.0 plotly==5.24.1
python -m streamlit run appInicio.py
```

La aplicación suele estar disponible en `http://localhost:8501`. Si el comando `py` no está disponible, utiliza `python` para crear el entorno. Si PowerShell bloquea la activación del entorno virtual, puedes omitir la activación y usar directamente:

```powershell
.\.venv\Scripts\python.exe -m pip install streamlit==1.47.0 plotly==5.24.1
.\.venv\Scripts\python.exe -m streamlit run appInicio.py
```

Invocar Streamlit mediante `python -m streamlit` ayuda a asegurar que se ejecute con el mismo intérprete en el que se instalaron las dependencias.

## Uso de la aplicación

1. Abre la sección **Cálculo del LCOH** desde el menú lateral o desde el botón de la página de inicio.
2. Ajusta los parámetros técnicos y económicos del formulario.
3. Pulsa **Calcular LCOH** para actualizar la estimación.
4. Consulta el resultado en USD/kg y los gráficos de distribución por componente.

La aplicación conserva el último resultado calculado en el estado de sesión de Streamlit.

## Parámetros de entrada

Los valores de la siguiente tabla son los valores iniciales del formulario:

| Grupo | Parámetro | Variable del modelo | Valor inicial | Unidad |
|---|---|---:|---:|---|
| CAPEX | Potencia del electrolizador | `p_el` | 1.000 | kW |
| CAPEX | Costo del electrolizador | `costo_el` | 1.345 | USD/kW |
| CAPEX | Factor de ingeniería | `a` | 0,19 | Proporción del costo directo |
| CAPEX | Factor de licencias | `b` | 0,01 | Proporción del costo directo |
| CAPEX | Factor de contingencias | `c` | 0,15 | Proporción del costo directo |
| OPEX | Eficiencia de la electrólisis | `efic_el` | 0,65 | Proporción |
| OPEX | Costo de electricidad (LCOE) | `LCOE` | 0,053 | USD/kWh |
| OPEX | Consumo de agua | `consumo_agua` | 15 | L/kg H₂ |
| OPEX | Precio del agua | `precio_agua` | 0,006 | USD/L |
| OPEX | Factor de mantenimiento | `psi` | 0,05 | Proporción del costo directo |
| Reemplazo | Factor del costo de reemplazo | `d` | 0,4 | Proporción del costo directo |
| Reemplazo | Año del reemplazo | `t` | 7 | Años |
| Producción | Consumo específico de energía del electrolizador | `PC` | 54 | kWh/kg H₂ |
| Producción | Horas de operación al año | `ha` | 8.760 | h/año |
| Economía | Tasa de descuento | `tasa_descuento` | 0,08 | Proporción |
| Economía | Vida del proyecto | `vida_proyecto` | 20 | Años |

El formulario limita la potencia a 100.000 kW y las horas anuales a un máximo de 8.760. La eficiencia y la tasa de descuento admiten valores entre 0 y 1. Para que el cálculo sea finito, no uses cero en la potencia, la eficiencia, el consumo específico de energía ni la tasa de descuento.

El campo `PC` aparece en la interfaz con la unidad `kW/kg`; el modelo y su documentación lo usan como consumo específico de energía en `kWh/kg H₂`.

## Método de cálculo implementado

El código calcula la producción anual como:

```text
Producción anual (kg H₂) = horas anuales × potencia × eficiencia / consumo específico
```

El costo directo de capital se obtiene multiplicando la potencia por el costo específico del electrolizador. Ingeniería, licencias y contingencias se calculan como proporciones de ese costo. El CAPEX se anualiza mediante el factor de recuperación de capital:

```text
CRF = i × (1 + i)^N / ((1 + i)^N − 1)
CAPEX anualizado = (costo directo + ingeniería + licencias + contingencias) × CRF
```

El OPEX anual suma el costo de electricidad, el costo de agua y el mantenimiento. El costo de reemplazo se descuenta desde el año indicado en el formulario y se anualiza con el mismo factor de recuperación. Finalmente:

```text
LCOH (USD/kg) = (CAPEX anualizado + OPEX anual + reemplazo anualizado)
                / producción anual de hidrógeno
```

En `Codigo\LCOH.py`, la función `calcular_costo_hidrogeno(...)` también devuelve un valor de LCOH en USD/L y datos de costos y producción. La interfaz actual muestra el valor en USD/kg y los gráficos en USD/kg; no presenta el valor en USD/L.

### Salidas visuales

- Resultado del costo total en USD/kg.
- Gráfico de barras apiladas con la contribución al LCOH del CAPEX, OPEX y reemplazo.
- Gráfico circular con la distribución porcentual de esos componentes.

## Supuestos y limitaciones

- El modelo calcula un escenario determinista con los parámetros introducidos en el formulario.
- Supone operación continua y estable de la planta, con demanda constante de hidrógeno.
- No modela la degradación progresiva de los electrolizadores ni las intermitencias del suministro eléctrico.
- No incorpora incentivos fiscales, deducciones tributarias, impuestos ni aranceles de importación.
- No incluye análisis de sensibilidad, simulaciones Monte Carlo ni optimización.
- Aunque la función de cálculo conserva un parámetro `fu`, no se expone en el formulario y no interviene en las ecuaciones implementadas.
- Los resultados dependen de los datos de entrada y no sustituyen un análisis financiero o de ingeniería específico del proyecto.

## Referencia bibliográfica mostrada en la página de inicio

Benalcazar, P. y Komorowska, A. (2024). “Techno-economic analysis and uncertainty assessment of green hydrogen production in future exporting countries”. *Renewable and Sustainable Energy Reviews*, 199, 114512.

El artículo reporta para Colombia un LCOH de USD 4,1–4,9/kg hacia 2030 en los escenarios que analiza. Ese intervalo es una referencia del estudio, no un rango universal ni una predicción de la calculadora. Los límites de alcance y los supuestos de ambos análisis deben tenerse en cuenta antes de comparar resultados.

## Estructura relevante

```text
.
├── appInicio.py       # Interfaz Streamlit: Inicio y Cálculo del LCOH
├── requerimientos.txt # Archivo de dependencias del proyecto
└── Codigo
    └── LCOH.py        # Función de cálculo y gráficos del LCOH
```

## Comprobaciones básicas

Desde la raíz del proyecto, verifica la sintaxis:

```powershell
python -m py_compile appInicio.py Codigo\LCOH.py
```

Comprueba que el cálculo y la creación de gráficos se pueden importar y ejecutar:

```powershell
python -c "from Codigo.LCOH import calcular_costo_hidrogeno, grafico_lcoh, grafico_lcoh_pie; r = calcular_costo_hidrogeno(); print('LCOH: {:.2f} USD/kg'.format(r['LCOH_kg'])); grafico_lcoh(r); grafico_lcoh_pie(r)"
```

## Solución de problemas

### `streamlit` no se reconoce o aparece `command not found`

Ejecuta Streamlit con el intérprete activo:

```powershell
python -m streamlit run appInicio.py
```

### `ModuleNotFoundError: No module named 'plotly'` o `streamlit`

Instala el paquete con el mismo intérprete que utilizarás para iniciar la aplicación:

```powershell
python -m pip install plotly==5.24.1 streamlit==1.47.0
python -m streamlit run appInicio.py
```

### `ModuleNotFoundError: No module named 'Codigo'`

Ejecuta el comando desde la raíz del proyecto y comprueba que existe `Codigo\LCOH.py`.
