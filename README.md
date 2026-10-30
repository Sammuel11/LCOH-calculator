# 🧬 HYDRA v2.0 - Hydrogen Diffusion and Risk Analyzer

## Quick Start

### 1. Requisitos Previos

- **Python:** 3.10 o superior
- **Sistema Operativo:** Windows, macOS, o Linux
- **Administrador de Paquetes:** Conda (recomendado) o pip

### 2. Instalación de Dependencias

#### Opción A: Conda (Recomendado - Especialmente para `assimulo` y `sundials`)

```bash
# Crear ambiente virtual
conda create -n hydra python=3.10 -y
conda activate hydra

# Instalar dependencias principales
conda install -c conda-forge streamlit==1.47.0 pandas==2.2.2 numpy==1.26.4 plotly==5.24.1 matplotlib==3.9.2 seaborn==0.13.2 scipy==1.13.1

# Instalar dependencias compiladas (críticas para módulos de fractura/ODE)
conda install -c conda-forge assimulo sundials

# Instalar componentes adicionales de Streamlit
pip install streamlit-plotly-events==0.0.6 streamlit-code-editor==0.1.22
```

#### Opción B: pip (Nota: Requiere compiladores del sistema para `assimulo` y `sundials`)

```bash
# Crear ambiente virtual (Python 3.10+)
python -m venv hydra_env
source hydra_env/bin/activate  # En Windows: hydra_env\Scripts\activate

# Instalar desde requerimientos.txt
pip install -r requerimientos.txt

# Si assimulo falla, instala las librerías compiladas vía conda en paralelo:
# conda install -c conda-forge assimulo sundials
```

### 3. Ejecutar la Aplicación

```bash
# Desde el directorio raíz del proyecto
streamlit run appInicio.py
```

**Resultado:** La interfaz se abrirá en `http://localhost:8501`

---

## 📋 Estructura de la Aplicación

```
calculadora_streamlit/
├── appInicio.py                          # Punto de entrada principal (Streamlit UI)
├── requerimientos.txt                    # Dependencias con versiones exactas
├── README.md                             # Este archivo
├── MEJORAS_DOCUMENTACION.md              # Registro de cambios recientes
├── tramos.csv                            # Datos de infraestructura de tubería
├── planimetria.png                       # Visualización esquemática de red
└── Codigo/
    ├── LCOH.py                          # Cálculo de costo nivelado de hidrógeno
    ├── Permeabilidadcosto_P_1090.py     # Análisis de pérdidas por difusión
    ├── difusionH2_stress_FD.py          # Simulación de esfuerzos mecánicos (FD)
    ├── pore_model_scipy_adsorption.py   # Modelo de poro (régimen elástico)
    ├── propagacion_fracturas.py         # Modelo de fractura (régimen plástico)
    ├── fractura_montecarlo.py           # Montecarlo de propagación de grietas
    ├── montecarlo_difusion_basico.py    # Montecarlo de acumulación de H₂
    ├── costos_diff_monteC_año.py        # Montecarlo de costos anuales
    ├── utils.py                         # Funciones auxiliares (CSS, formato)
    └── estilos.css                      # Estilos personalizados
```

---

## 🎯 Menús Principales

### 1. **Inicio** 🏠
Pantalla de bienvenida con:
- Descripción de HYDRA y contexto del proyecto (UPB-EPM)
- Vista general de 8 módulos principales
- Acotaciones técnicas
- Call-to-action hacia módulos específicos
- Pie de página con créditos

### 2. **Cálculo del LCOH** 💰
Análisis económico integrado del costo nivelado de hidrógeno.

**Parámetros:**
- CAPEX: Potencia (kW), costo específico, ingeniería, licencias, contingencias
- OPEX: Eficiencia (%), LCOE (USD/kWh), agua, mantenimiento
- Reemplazo: Factor de degradación y período (años)
- Económicos: Tasa de descuento (%), vida útil (años)

**Salidas:** Gráficos de distribución de costo, análisis de sensibilidad

### 3. **Pérdidas y Costos** 📉
Cuantificación de fugas por difusión molecular a través de paredes.

**Características:**
- Análisis multi-tramo: Producción, Transporte, Distribución
- Variación temporal: Envejecimiento de materiales
- Múltiples gases: H₂, H₂GN, CH₄
- Sensibilidad: Presión, temperatura, espesor

**Salidas:** Tablas de pérdidas, gráficos de costos acumulativos

### 4. **Montecarlo Pérdidas y Costos** 🎲
Análisis probabilístico de costos con incertidumbre de parámetros.

**Incluye:**
- Distribuciones de parámetros inciertos (uniforme, normal, etc.)
- Número de simulaciones: 100–20,000
- Estadísticos: Media, desv. std., percentiles
- Identificación de escenarios críticos (worst-case)

**Salidas:** Histogramas, curvas de distribución, tornado plots

### 5. **Acumulación en Recintos Cerrados** 📦
Evaluación de riesgo de explosividad en espacios confinados.

**Evaluación:**
- Concentración de H₂ vs. LEL (4% en aire)
- Probabilidad de excedencia
- Impacto de ventilación
- Recomendaciones de diseño

**Salidas:** Gráficos de concentración vs. tiempo, matriz de riesgo

### 6. **Esfuerzos Mecánicos** ⚙️
Análisis de tensiones, deformaciones y factores de seguridad.

**Método:** Diferencias finitas con acoplamiento tensión-difusión

**Resultados:**
- Esfuerzo von Mises (Pa)
- Factor de seguridad (FS) vs. límite elástico
- Evolución temporal
- Mapas de criticidad por tramo

**Salidas:** Gráficos 2D/3D, series de tiempo

### 7. **Régimen Elástico y Plástico** 🔄💥
Modelado de deformación reversible e irreversible con adsorción.

**Régimen Elástico:**
- Comportamiento reversible (Hooke)
- Adsorción de H₂ en poros
- Acumulación de presión interna
- Deformación volumétrica

**Régimen Plástico:**
- Daño permanente acumulativo
- Propagación de grietas por fatiga
- Criterios de fractura energéticos
- Vida residual predicha

**Salidas:** Subplots 2×2 (presión poro, fracción ocupada, deformación, daño)

### 8. **Montecarlo Poro (Fractura)** 💥
Análisis probabilístico de propagación de grietas bajo incertidumbre.

**Cuantifica:**
- Tiempo a fallo (TTF) para cada tramo
- Confiabilidad por año (%)
- Sensibilidad de parámetros
- Escenarios worst-case y best-case
- Curvas de supervivencia

**Salidas:** Histogramas TTF, curvas de confiabilidad, Pareto de incertidumbre

---

## 🔧 Convenciones y Especificaciones del Proyecto

### Lenguaje y Estilo
- **Código:** Español para variables, funciones y comentarios (preservar conocimiento del dominio)
- **Mensajes UI:** Español en la interfaz Streamlit
- **Documentación:** Español en archivos .md

### Unidades Estándar
| Magnitud | Unidad | Notas |
|----------|--------|-------|
| Temperatura | K (Kelvin) | 273.15 K = 0 °C |
| Presión | Pa (Pascales) | 1 bar = 100,000 Pa |
| Longitud | m (metros) | Diámetro, espesor, distancia |
| Costo Hidrógeno | USD/kg o USD/L | LCOH (Levelized Cost of Hydrogen) |
| Coeficiente Difusión | m²/s | Típico: 10⁻¹⁰ m²/s |
| Permeabilidad | mol/(m·s·Pa^0.5) | Ley de Sieverts |

### Estructura de Código
- **Funciones de cálculo:** Retornan `dict`, `DataFrame` (pandas) o `Figure` (plotly)
- **No hay llamadas `.show()`:** Streamlit renderiza figuras automáticamente
- **Importaciones:** `from Codigo import modulo` (desde raíz del proyecto)
- **Archivo de configuración:** `st.session_state` para cache de resultados

### Archivos de Datos
- **tramos.csv:** Separador `;` (punto y coma), codificación UTF-8
- **planimetria.png:** Ruta relativa desde raíz

---

## 📚 Referencias Técnicas y Bibliografía

| Tema | Referencia |
|------|-----------|
| **LCOH** | DOE Hydrogen and Fuel Cell Technologies Office, *Cost Analysis Framework*, 2020 |
| **Difusión Molecular** | Crank, J. *Mathematics of Diffusion*. Oxford UP, 1975 |
| **Mecánica de Fractura** | Griffith, A.A. *The phenomenon of rupture and flow in solids*. RSPA, 1920 |
| **Fragilización por H₂** | SAE J2340: *Hydrogen Compatibility of Elastomers and Plastics*, 2013 |
| **Método de Montecarlo** | Metropolis & Ulam. *The Monte Carlo method*. JASA, 1949 |
| **Modelos de Adsorción** | Langmuir, I. *Adsorption of Gases*. JACS, 1918 |

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'assimulo'"
```bash
# Solución: Instalar desde conda-forge
conda install -c conda-forge assimulo sundials
```
**Causa:** `assimulo` contiene binarios compilados; pip a veces falla.

### Error: "FileNotFoundError: tramos.csv"
```bash
# Asegúrate de ejecutar desde el directorio raíz del proyecto
cd c:\Users\SEC07\calculadora_streamlit  # Ejemplo en Windows
streamlit run appInicio.py
```
**Causa:** Las rutas de archivo son relativas a la raíz del proyecto.

### Error: "StreamlitAPIException: Invalid value for 'column' parameter"
```bash
# Actualiza Streamlit
pip install --upgrade streamlit
```
**Causa:** Versión de Streamlit desactualizada.

### Error: "ImportError: cannot import name 'Figure' from plotly.graph_objects"
```bash
# Asegúrate de tener la versión correcta de Plotly
pip install --upgrade plotly==5.24.1
```

### Rendimiento Lento
- **Verificar:** `st.session_state` para caché; si el caché es antiguo, limpiarlo
- **Optimizar:** Reducir número de simulaciones en Montecarlo de prueba
- **GPU (opcional):** No se utiliza en esta versión

---

## � Validación y Testing

### Smoke Tests (Manual)

Verificar que la instalación es correcta:

```bash
# Test 1: Cálculo LCOH básico
python -c "from Codigo.LCOH import calcular_costo_hidrogeno; print(calcular_costo_hidrogeno())"

# Test 2: Pérdidas de difusión
python -c "from Codigo.Permeabilidadcosto_P_1090 import calcular_perdidas; print(calcular_perdidas())"

# Test 3: Esfuerzos mecánicos
python -c "import Codigo.difusionH2_stress_FD as d; res = d.esfuerzos(); print(list(res.keys()))"

# Test 4: Modelo elástico
python -c "import Codigo.pore_model_scipy_adsorption as p; res = p.poro_ad_model(); print('OK')"

# Test 5: Modelo plástico (fractura)
python -c "import Codigo.propagacion_fracturas as pf; res = pf.poro_assi_fract(); print('OK')"
```

---

## 📧 Soporte y Contacto

**Contacto Técnico:** samuel.rodriguezs@upb.edu.co

**Instituciones:**
- Universidad Pontificia Bolivariana (UPB) - Medellín, Colombia
- Empresas Públicas de Medellín (EPM) - Operador de Infraestructura

**Equipo Técnico:**
- Investigación: Laboratorio de Energías Alternativas (UPB)
- Validación: Departamento de Ingeniería (EPM)

---

## 📄 Licencia y Créditos

© 2025-2026 Universidad Pontificia Bolivariana & Empresas Públicas de Medellín

- **Versión:** 2.0
- **Fecha de Lanzamiento:** Enero 2026
- **Estado:** Producción
- **Python:** 3.10+

---

## ✨ Novedades en v2.0

- ✅ Rediseño completo del menú "Inicio" con estética profesional
- ✅ Descripciones técnicas ampliadas para todos los 8 módulos
- ✅ Mejora de coherencia y lenguaje técnico
- ✅ Actualización de `requerimientos.txt` con versiones exactas
- ✅ Documentación de cambios en `MEJORAS_DOCUMENTACION.md`
- ✅ Estilos CSS profesionales (gradientes, tipografía)
- ✅ Iconos emoji consistentes en menús
- ✅ README.md completo con instrucciones exactas y troubleshooting

---

¡Disfruta analizando infraestructuras de transporte de hidrógeno con HYDRA! 🚀

Para contribuir o reportar errores, abre un issue en el repositorio interno de UPB.
