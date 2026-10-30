# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 16:27:04 2025

@author: SEC07
"""
import plotly.graph_objects as go

def calcular_costo_hidrogeno(
    # Parámetros 
    
    # CAPEX
    p_el: float = 1000,               # potencia del electrolizador
    costo_el: float = 1345,           # costo del electrolizador [USD/kW]
    vida_proyecto: int = 20,        # Años de operación
    
    # OPEX
    efic_el: float = 0.65,             # Eficiencia de la electrolisis
    fu: float =1,                  # factor de utilizacion
    LCOE: float = 0.053,                # [USD/kWh]
    consumo_agua: float = 15,        # [L/kg_H2]
    precio_agua: float =0.006,         # [USD/L]
    psi: float = 0.05,             # % del capex directo asociado a los costos variables de operacion y mantenimeinto
    d: float = 0.4,               # % del capex directo asociado al costo de remplazo del electrolizador
    t: float = 7,                   # tasa de remplazo del electrolizador
    
    # Producción anual de H2
    PC: float = 54,                   # consumo de enrgia del electrolizador 
    ha: float = 8760,            # numero de horas en el año
    
    # Parametro economico
    tasa_descuento: float = 0.08,  # Tasa de descuento 
    a: float = 0.19,               # factor destinado a los costos de ingenieria 
    b: float = 0.01,               # factor destinado a los costos de lisencias
    c: float = 0.15,               # factor destinado a los costos de contingencias del proyecto
    
) -> dict:
    
    """
    Calculo del costo nivelado de hidrógeno (LCOH) 
    """

    Mwh2 = 2.016e-3         # Masa molar del H2 [kg/mol]
    
    # 1. Cálculo del LCOH (Costo Nivelado de Hidrógeno)
    factor_recuperacion = (tasa_descuento * (1 + tasa_descuento)**vida_proyecto) / \
                        ((1 + tasa_descuento)**vida_proyecto - 1)
    
    # 1.1 Calculo CAPEX anualizado
    costo_directo = costo_el*p_el
    capex_construccion = a*costo_directo
    capex_inge = b*costo_directo
    capex_contingencia = c*costo_directo
    
    CAPEX = (costo_directo + (capex_construccion + capex_inge + capex_contingencia))*factor_recuperacion
    
    #1.2 Calculo produccion anualizada de H2
    
    prod_h2_kg = (ha*p_el*efic_el)/PC # [kg_H2]
    prod_h2_L= (prod_h2_kg/Mwh2)*22.4 # [L_H2]
    
    
    #1.3 Calculo OPEX anualizado
    costo_energia= ha*p_el*efic_el*LCOE
    costo_agua= consumo_agua*precio_agua*prod_h2_kg
    costo_ope_mante= costo_directo*psi
    
    OPEX = costo_energia + costo_agua + costo_ope_mante
    
    #1.4 Calculo costo remplazo anualizado
    costo_remp= d*costo_directo
    remp= ((costo_remp)/((1+tasa_descuento)**t))*factor_recuperacion
    
    LCOH_kg = (CAPEX+OPEX+remp)/prod_h2_kg # [USD/Kg]
    LCOH_L = (CAPEX+OPEX+remp)/prod_h2_L   # [USD/L]
    
    capexp = (CAPEX)/prod_h2_kg
    opexp = (OPEX)/prod_h2_kg
    rempp = (remp)/prod_h2_kg
    
    return{
        'LCOH_kg': LCOH_kg,
        'LCOH_L': LCOH_L,
        'Capex': costo_directo + (capex_construccion + capex_inge + capex_contingencia),
        'Capex_anual': CAPEX,
        'Opex_anual': OPEX,
        'Costo_energia_anual': costo_energia,   
        'Costo_agua_anual': costo_agua,    
        'capex_lcoh': capexp,
        'opex_lcoh': opexp,
        'remplazo_lcoh' : rempp
        } 

# Gráfico de barras para la distribución del LCOH por componente
def grafico_lcoh(resultado):
    categorias = ['CAPEX', 'OPEX', 'Remplazo']
    valores = [resultado['capex_lcoh'], resultado['opex_lcoh'], resultado['remplazo_lcoh']]

    fig = go.Figure()
    fig.add_trace(go.Bar(name='CAPEX',x=['LCOH_kg'], y=[valores[0]], marker_color='green'))
    fig.add_trace(go.Bar(name='OPEX', x=['LCOH_kg'], y=[valores[1]], marker_color='lightgreen'))
    fig.add_trace(go.Bar(name='Remplazo', x=['LCOH_kg'], y=[valores[2]], marker_color='springgreen'))

    fig.update_layout(
        barmode='stack',
        title='Distribución del LCOH por componente',
        xaxis_title='',
        yaxis_title='USD/kg H2',
        legend_title='Componente',
        font=dict(size=16),
        height=500,
        width=700
    )
    return fig
    

def grafico_lcoh_pie(resultado):
    categorias = ['CAPEX', 'OPEX', 'Remplazo']
    valores = [resultado['capex_lcoh'], resultado['opex_lcoh'], resultado['remplazo_lcoh']]

    fig = go.Figure(
        [go.Pie(labels=categorias, values=valores, hole=0.5, textinfo='percent+label', marker=dict(colors=['green','lightgreen','springgreen']))])
    fig.update_layout(
        title='Distribución porcentual del LCOH por componente',
        font=dict(size=16),
        height=500,
        width=700
    )
    return fig
#%% 

# # Ejemplo Colombia
resultado = calcular_costo_hidrogeno(
    
#     # CAPEX
#     p_el = 1000,            # Potencia del electrolizador [kW]
#     costo_el = 1345,        # Costo del electrolizador [USD/kW]
#     vida_proyecto = 20,     # Años de operación
#     a = 0.19,               # Factor destinado a los costos de ingenieria 
#     b = 0.01,               # Factor destinado a los costos de lisencias
#     c = 0.15,               # Factor destinado a los costos de contingencias
    
#     # OPEX
#     efic_el = 0.65,          #  
#     fu = 1,                  # Factor de utilizacion
#     LCOE = 0.053,            # [USD/kWh]
#     consumo_agua = 15 ,      # [L/kg_H2]
#     precio_agua = 0.006 ,    # [USD/L]
#     psi = 0.05 ,      # % del capex directo asociado a los costos variables de operacion y mantenimeinto
#     d = 0.4,                 # % del capex directo asociado al costo de remplazo del electrolizador
#     t = 7,                   # Tasa de remplazo del electrolizador
    
#     # Producción anual de H2
#     PC = 54,                   # Consumo de enrgia del electrolizador 
#     ha = 8760,                 # Numero de horas en el año
    
#     # Parametro economico
#     tasa_descuento = 0.08,   # Tasa de descuento 
    
)

# # #Resultados
# print(f"Costo de producción (LCOH): ${resultado['LCOH_kg']:.2f} USD/kg")
# print(f"Costo de producción (LCOH): ${resultado['LCOH_L']:.5f} USD/lt")

# # Mostrar el gráfico
# figura=grafico_lcoh(resultado)
# figurapie=grafico_lcoh_pie(resultado)
# figurapie.show()