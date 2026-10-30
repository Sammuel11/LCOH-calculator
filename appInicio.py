import streamlit as st
import Codigo.LCOH as LCOH  

#Interfaz
# Inicializar el estado del menú si no existe
if 'menu' not in st.session_state:
    st.session_state['menu'] = "Inicio"
st.set_page_config(layout="wide")
menu = st.sidebar.radio(
    "Menú de opciones",
    (
        "Inicio",
        "Cálculo del LCOH",
        # "Matriz para la clasificación del riesgo"
        
    ),
    index=["Inicio", "Cálculo del LCOH"].index(st.session_state['menu'])
)

# Contenido para el menú de Inicio
if menu == "Inicio":
    # Estilos CSS personalizados
    st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
        }
        
        .header-section {
            background: linear-gradient(135deg, #0f3460 0%, #1a5f7a 100%);
            color: white;
            padding: 60px 40px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .header-section h1 {
            font-size: 3.5em;
            font-weight: 800;
            margin-bottom: 15px;
            letter-spacing: -1px;
        }
        
        .header-section .subtitle {
            font-size: 1.3em;
            font-weight: 300;
            margin-bottom: 10px;
            opacity: 0.95;
            line-height: 1.6;
        }
        
        .value-proposition {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
            border-left: 4px solid #4fc3f7;
            font-style: italic;
            font-size: 1.1em;
        }
        
        .context-block {
            background-color: #f8f9fa;
            border-left: 5px solid #0f3460;
            padding: 25px;
            margin: 30px 0;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .context-block h3 {
            color: #0f3460;
            margin-bottom: 15px;
            font-size: 1.5em;
        }
        
        .context-block p {
            color: #2c3e50;
            line-height: 1.8;
            margin-bottom: 12px;
            font-size: 1.05em;
        }
        
        .context-block ul {
            margin-left: 20px;
            color: #2c3e50;
            line-height: 1.9;
        }
        
        .context-block li {
            margin-bottom: 10px;
            font-size: 1.05em;
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .feature-card {
            background: white;
            border-radius: 10px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-top: 4px solid #4fc3f7;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }
        
        .feature-card .icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        
        .feature-card h4 {
            color: #0f3460;
            margin-bottom: 12px;
            font-size: 1.3em;
            font-weight: 700;
        }
        
        .feature-card p {
            color: #555;
            font-size: 0.95em;
            line-height: 1.6;
        }
        
        .limitations-block {
            background-color: #fff3e0;
            border-left: 5px solid #ff9800;
            padding: 25px;
            margin: 30px 0;
            border-radius: 8px;
        }
        
        .limitations-block h3 {
            color: #e65100;
            margin-bottom: 15px;
            font-size: 1.5em;
        }
        
        .limitations-block ul {
            margin-left: 20px;
            color: #424242;
            line-height: 1.9;
        }
        
        .limitations-block li {
            margin-bottom: 10px;
            font-size: 1.05em;
        }
        
        .partners-section {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 40px;
            border-radius: 10px;
            margin: 30px 0;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        
        .partners-section h3 {
            color: #0f3460;
            margin-bottom: 30px;
            font-size: 1.8em;
            font-weight: 700;
        }
        
        .partners-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
        }
        
        .partner-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .partner-card h4 {
            color: #0f3460;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .partner-card p {
            color: #666;
            font-size: 0.95em;
            line-height: 1.6;
        }
        
        .cta-section {
            background-color: #0f3460;
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin: 30px 0;
            text-align: center;
        }
        
        .cta-section h3 {
            margin-bottom: 25px;
            font-size: 1.8em;
            font-weight: 700;
        }
        
        .button-group {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .footer-section {
            background-color: #1a2a3a;
            color: #ecf0f1;
            padding: 40px;
            border-radius: 10px;
            margin: 30px 0;
            margin-top: 50px;
        }
        
        .footer-section h4 {
            color: #4fc3f7;
            margin-bottom: 15px;
            font-size: 1.1em;
            font-weight: 700;
        }
        
        .footer-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
        }
        
        .footer-column p, .footer-column a {
            color: #ecf0f1;
            margin-bottom: 8px;
            font-size: 0.95em;
            line-height: 1.8;
        }
        
        .footer-column a {
            color: #4fc3f7;
            text-decoration: none;
            font-weight: 500;
        }
        
        .footer-column a:hover {
            text-decoration: underline;
        }
        
        .divider {
            border-top: 2px solid rgba(79,195,247,0.3);
            margin: 30px 0;
        }
        
        .badge {
            display: inline-block;
            background-color: #4fc3f7;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin: 5px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # === ENCABEZADO PRINCIPAL ===
    col1, col2 = st.columns([1,2.5])
    st.markdown("""
    <div class="header-section">
        <h1>🧬 LCOH</h1>
        <div class="subtitle">Calculadora del costo nivelado de hidrógeno</div>
        <div class="value-proposition">
            Estima el costo de producción del hidrógeno durante la vida útil del proyecto y analiza la contribución de sus principales componentes.
        </div>
    </div>
    """, unsafe_allow_html=True)
    # col1.image("Logohydra1.png", width=350)


    # === CONTEXTO DEL PROYECTO ===
    st.markdown("""
    <div class="context-block">
        <h3>📌 Contexto de la calculadora</h3>
        <p>
            El costo nivelado de hidrógeno (LCOH, por sus siglas en inglés) expresa el costo promedio de producir una unidad de hidrógeno durante la vida útil de un proyecto. Esta calculadora estima el resultado en USD/kg y USD/L a partir de los costos anualizados y de la producción anual.
        </p>
        <h4 style="color: #0f3460; margin-top: 20px; margin-bottom: 10px; font-size: 1.2em;">Problema identificado</h4>
        <p>
            El LCOH depende de las condiciones técnicas, energéticas y financieras de cada proyecto. En particular, el costo de inversión del electrolizador y su nivel de utilización pueden cambiar de forma importante el costo estimado; por ello, un valor aislado no representa todos los escenarios posibles.
        </p>
        <h4 style="color: #0f3460; margin-top: 20px; margin-bottom: 10px; font-size: 1.2em;">Solución propuesta</h4>
        <p>
            La herramienta permite modificar parámetros del electrolizador y del proyecto para estimar el costo nivelado y visualizar la participación del CAPEX, el OPEX y el reemplazo. El cálculo considera, entre otros elementos, inversión, ingeniería, licencias, contingencias, energía, agua, mantenimiento y reposición del electrolizador.
        </p>
        <h4 style="color: #0f3460; margin-top: 20px; margin-bottom: 10px; font-size: 1.2em;">Referencia de la literatura</h4>
        <p>
            El estudio de Benalcazar y Komorowska (2024) analizó la producción de hidrógeno verde con energía solar y eólica en 76 sitios de Australia, Chile, Colombia y Marruecos. Para Colombia, reportó un LCOH de USD 4,1–4,9/kg hacia 2030. El análisis también identificó el costo específico de inversión y la utilización del electrolizador como factores especialmente influyentes.
        </p>
        <p>
            Referencia: P. Benalcazar y A. Komorowska, “Techno-economic analysis and uncertainty assessment of green hydrogen production in future exporting countries”, <em>Renewable and Sustainable Energy Reviews</em>, vol. 199, 2024, artículo 114512.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # === LIMITACIONES Y SUPUESTOS TÉCNICOS ===
    st.markdown("""
    <div class="limitations-block">
        <h3>⚠️ Limitaciones y Supuestos</h3>
        <h4 style="color: #e65100; margin-top: 15px; margin-bottom: 10px; font-size: 1.15em;">Supuestos del modelo</h4>
        <ul>
            <li>Se asume que la planta opera de forma continua y estable, con una demanda constante de hidrógeno.</li>
            <li>No se modelan la degradación progresiva de los electrolizadores ni las intermitencias del suministro eléctrico.</li>
            <li>No se incluyen incentivos fiscales, deducciones tributarias, impuestos ni aranceles de importación o sus posibles exenciones.</li>
        </ul>
        <h4 style="color: #e65100; margin-top: 15px; margin-bottom: 10px; font-size: 1.15em;">Interpretación de los resultados</h4>
        <ul>
            El intervalo de USD 4,1–4,9/kg corresponde a los escenarios para Colombia hacia 2030 del estudio citado; es una referencia de la literatura, no un rango teórico universal ni un resultado garantizado por esta calculadora. Incorporar los factores excluidos o actualizar los supuestos locales puede cambiar el LCOH y ubicarlo dentro o fuera de ese intervalo. Para decisiones de inversión, se recomienda verificar los datos y supuestos con información específica del proyecto.
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # === FUNCIONALIDADES PRINCIPALES ===
    st.markdown("""
    <h2 style="text-align: center; color: #0f3460; margin: 40px 0 30px 0;">🎯 Funcionalidades Principales</h2>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    </div>
    <div class="feature-grid">
        <div class="feature-card">
            <div class="icon">💰</div>
            <h4>Cálculo del LCOH</h4>
            <p>Análisis económico integrado del costo nivelado de hidrógeno considerando inversión inicial, operación, mantenimiento y remplazo de componentes a lo largo de la vida útil del proyecto.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    
    # === CALL TO ACTIONS ===
    st.markdown("""
    <div class="cta-section">
        <h3>🚀 Comienza tu Análisis Ahora</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Botones de navegación en columnas
    cols = st.columns(1)
    
    with cols[0]:
        if st.button("💰 LCOH", use_container_width=True, key="btn_lcoh"):
            st.session_state['menu'] = "Cálculo del LCOH"
            st.rerun()
    
    # === PIE DE PÁGINA (FOOTER) ===
    st.markdown("""
    <div class="footer-section">
        <div class="footer-content">
            <div class="footer-column">
                <h4>📧 Contacto</h4>
                <p>Para consultas técnicas:</p>
                <a href="mailto:soporte.tecnico@empresa.co">
                    📧 soporte.tecnico@empresa.co
                </a>
            </div>
            <div class="footer-column">
                <h4>📚 Documentación</h4>
                <p>Accede a guías técnicas, manuales de usuario y artículos de investigación:</p>
                <p>🔬 Papers técnicos y validaciones</p>
            </div>
            <div class="footer-column">
                <h4>ℹ️ Información del Software</h4>
                <p><strong>Versión:</strong> 1.0</p>
                <p><strong>Última actualización:</strong> Enero 2026</p>
                <p><strong>Licencia:</strong> Desarrollo y Validación</p>
                <p style="margin-top: 15px; font-size: 0.9em; opacity: 0.8;">
                    © 2025-2026
                    Todos los derechos reservados.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if menu == "Cálculo del LCOH":
    st.title("💰 Cálculo del Costo Nivelado de Hidrógeno (LCOH)")
    st.markdown(
        "Ajusta los parámetros técnicos y económicos y pulsa **Calcular LCOH** "
        "para actualizar la estimación con los supuestos seleccionados."
    )
    with st.form("form_lcoh"):
        st.header("Variables de entrada")
        with st.container():
            st.subheader("Variables del CAPEX")
            col1, col2, col3 = st.columns(3)
            # Entradas para los parámetros de la función
            p_el = col1.number_input("Potencia del electrolizador (kW)", min_value=0.0, value=1000.0, max_value=100000.0)
            costo_el = col2.number_input("Costo del electrolizador (USD/kW)", min_value=0.0, value=1345.0)
            a = col3.number_input("Factor costos ingeniería", min_value=0.0, value=0.19,)
        with st.container():
            col1, col2 = st.columns(2)
            b = col1.number_input("Factor costos licencias", min_value=0.0, value=0.01)
            c = col2.number_input("Factor costos contingencias", min_value=0.0, value=0.15)
        with st.container():
            st.subheader("Parámetros del OPEX")
            col1, col2, col3 = st.columns(3)
            efic_el = col1.number_input("Eficiencia de la electrólisis", min_value=0.0, max_value=1.0, value=0.65)
            LCOE = col2.number_input("LCOE (USD/kWh)", min_value=0.0, value=0.053,format="%.3f")
            consumo_agua = col3.number_input("Consumo de agua (L/kg_H2)", min_value=0.0, value=15.0)
        with st.container():
            col1, col2 = st.columns(2)
            precio_agua = col1.number_input("Precio del agua (USD/L)", min_value=0.0, value=0.006)
            psi = col2.number_input("Factor costos de mantenimiento", min_value=0.0, value=0.05)
        with st.container():
            st.subheader("Parámetros de remplazo")
            col1, col2 = st.columns(2)
            d = col1.number_input("Factor costo del remplazo", min_value=0.0, value=0.4)
            t = col2.number_input("Tasa de remplazo (años)", min_value=1.0, value=7.0)
        with st.container():
            st.subheader("Parámetros de producción")
            col1, col2 = st.columns(2)
            PC = col1.number_input("Consumo de energía del electrolizador (kW/kg)", min_value=0.0, value=54.0)
            ha = col2.number_input("Horas al año", min_value=1.0, value=8760.0, max_value=8760.0)
        with st.container():
            st.subheader("Parámetros económicos")    
            col1, col2 = st.columns(2)
            tasa_descuento = col1.number_input("Tasa de descuento", min_value=0.0, max_value=1.0, value=0.08)
            vida_proyecto = col2.number_input("Años de operación", min_value=1, value=20)

        boton_calcular = st.form_submit_button("Calcular LCOH")
    # Solo calcula si el usuario presiona el botón
    if boton_calcular:
        resultado = LCOH.calcular_costo_hidrogeno(
            p_el=p_el,
            costo_el=costo_el,
            vida_proyecto=int(vida_proyecto),
            efic_el=efic_el,
            LCOE=LCOE,
            consumo_agua=consumo_agua,
            precio_agua=precio_agua,
            psi=psi,
            d=d,
            t=t,
            PC=PC,
            ha=ha,
            tasa_descuento=tasa_descuento,
            a=a,
            b=b,
            c=c
        )
        st.session_state['lcoh_resultado'] = resultado
    else:
        resultado = st.session_state.get('lcoh_resultado', LCOH.calcular_costo_hidrogeno())

    st.write(f"Costo total (USD/kg): {resultado['LCOH_kg']:.2f}")
    resultado= st.session_state.get('lcoh_resultado', LCOH.calcular_costo_hidrogeno())
    st.session_state['costo_total_lcoh'] = resultado['LCOH_kg']
    st.session_state['costo_total_lcoh_l'] = resultado['LCOH_L']

    # Gráfico de barras para la distribución del LCOH por componente
    col1, col2 = st.columns((1.15,2))
    with col1:
        figura = LCOH.grafico_lcoh(resultado)
        st.plotly_chart(figura, use_container_width=True)
    with col2:
        figura_pie=LCOH.grafico_lcoh_pie(resultado)
        st.plotly_chart(figura_pie, use_container_width=True)