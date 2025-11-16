import streamlit as st
import pandas as pd
from PIL import Image
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io
import plotly.graph_objects as go

st.set_page_config(page_title="Plataforma de Indicadores Intangibles y Rentabilidad", layout="wide")
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"

def cambiar_pagina(pagina):
    st.session_state.pagina = pagina

# --- NUEVO: Solo efectos de animación (CSS) ---
def aplicar_animaciones_css():
    st.markdown("""
    <style>
    /* ===================== Animaciones globales ===================== */
    @keyframes fadeInUp {
        from {opacity: 0; transform: translate3d(0, 12px, 0);}
        to {opacity: 1; transform: translate3d(0, 0, 0);}
    }
    @keyframes floaty {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
        100% { transform: translateY(0px); }
    }
    @keyframes pulseRing {
        0% { box-shadow: 0 0 0 0 rgba(29,78,216,.35); } /* azul-700 */
        70% { box-shadow: 0 0 0 12px rgba(29,78,216,0); }
        100% { box-shadow: 0 0 0 0 rgba(29,78,216,0); }
    }

    /* Contenedor principal entra suavemente */
    .block-container { animation: fadeInUp .6s ease both; }

    /* Imagen del sidebar con flotación sutil (si existiera) */
    [data-testid="stSidebar"] img { animation: floaty 4s ease-in-out infinite; }

    /* Título principal (tu h1 con estilo inline) también se anima */
    div.stMarkdown h1 { animation: fadeInUp .8s ease both; }

    /* Tarjetas/alertas y bloques aparecen con fadeInUp */
    .stAlert, .stMarkdown, .stPlotlyChart, .element-container { animation: fadeInUp .6s ease both; }

    /* Campos numéricos y select con focus suave (azul corporativo) */
    div[data-testid="stNumberInput"] input, div[data-testid="stSelectbox"] select {
        transition: box-shadow .25s ease, transform .12s ease;
    }
    div[data-testid="stNumberInput"] input:focus, div[data-testid="stSelectbox"] select:focus {
        box-shadow: 0 0 0 3px rgba(29,78,216,.25); /* azul-700 */
        transform: translateY(-1px);
    }

    /* Tus cajas de resultados .readonly con animación */
    .readonly { animation: fadeInUp .7s ease both; }

    /* Botones: sin cambiar lógica, solo animación y sombra corporativa */
    div.stButton > button {
        transition: transform .15s ease, box-shadow .25s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(17,24,39,.15); /* gris-900 */
    }
    div.stButton > button:active {
        transform: translateY(0);
        animation: pulseRing .9s ease;
    }

    /* Gráficos Plotly con animación de entrada */
    .stPlotlyChart { animation-delay: .05s; }

    /* Ligeras demoras para columnas (efecto cascada) */
    div[data-testid="column"]:nth-child(1) { animation-delay: 0.05s; }
    div[data-testid="column"]:nth-child(2) { animation-delay: 0.10s; }
    div[data-testid="column"]:nth-child(3) { animation-delay: 0.15s; }
    div[data-testid="column"]:nth-child(4) { animation-delay: 0.20s; }
    </style>
    """, unsafe_allow_html=True)

def mostrar_inicio():   
    # Crear columnas para imagen y texto principal
    col1, col2 = st.columns([1, 2])

    with col1:
        img = Image.open("UTA.png")
        st.image(img, width=250)

    with col2:
        st.markdown("""
        <h1 style='font-size: 32px; color: #1f2937;'>
            📊 Plataforma de Indicadores Intangibles y Rentabilidad
        </h1>
        <p style='font-size: 18px; color:#374151;'>
            <strong>Proyecto de investigación:</strong> 
            <em>Métricas intangibles y rentabilidad de las empresas que cotizan en la bolsa de valores del Ecuador</em>
        </p>
        """, unsafe_allow_html=True)

    # Texto introductorio
    st.markdown("""
    <p style='font-size:16px; text-align: justify; color:#374151;'>
    Esta aplicación permite calcular automáticamente los principales indicadores relacionados con el capital intelectual y la rentabilidad de las empresas ecuatorianas que cotizan en bolsa. 
    Podrás cargar un archivo con los datos financieros de las empresas y obtener:
    </p>
    """, unsafe_allow_html=True)

    # Indicadores
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        #### 📌 Indicadores de Capital Intelectual:
        - 🧠 Valor Añadido (VA)  
        - 👥 Eficiencia del Capital Humano (HCE)  
        - 🏢 Eficiencia del Capital Estructural (SCE)  
        """)

    with col4:
        st.markdown("""
        #### 📌 Indicadores de Rentabilidad:
        - 📈 Índice de Valor Añadido Intelectual (VAIC™)  
        - 💹 Rentabilidad sobre Activos (ROA)  
        - 💰 Rentabilidad sobre el Patrimonio (ROE)  
        """)

    # Cierre
    st.markdown("""
    <p style='font-size:16px; color:#374151;'>
    Además, podrás visualizar resultados y exportarlos fácilmente.
    </p>
    """, unsafe_allow_html=True)

    # Frase inspiradora
    st.info("💡 “El conocimiento se ha convertido en el activo más valioso de la economía actual.” — Stewart, 1997")

def mostrar_indicadores():
    st.title("📊 Indicadores calculados")
    
    # CSS para estilizar las cajas de texto, etiquetas no editables, selectbox y botón (paleta corporativa)
    st.markdown("""
    <style>
        div[data-testid="stNumberInput"] input {
            font-size: 20px !important;
            padding: 10px !important;
            border: 2px solid #1D4ED8 !important; /* azul-600 */
            border-radius: 8px !important;
            background-color: #ffffff !important;
            color: #111827 !important; /* gris-900 */
            width: 100% !important;
        }
        div[data-testid="stNumberInput"] label {
            font-size: 20px !important;
            color: #111827 !important;
            font-weight: bold !important;
            text-align: center !important;
        }
        div[data-testid="column"] .stMarkdown.readonly {
            font-size: 20px !important;
            padding: 10px !important;
            border: 2px solid #E5E7EB !important; /* gris-200 */
            border-radius: 8px !important;
            background-color: #F8FAFC !important; /* slate-50 */
            color: #111827 !important;
            margin-bottom: 10px !important;
            text-align: center !important;
        }
        div.stButton > button {
            font-size: 20px !important;
            padding: 10px !important;
            border: 2px solid #1E3A8A !important; /* azul-800 */
            border-radius: 8px !important;
            background-color: #1D4ED8 !important; /* azul-600 */
            color: #ffffff !important;
            width: 100% !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover {
            background-color: #1E40AF !important; /* azul-700 */
            color: #ffffff !important;
            border-color: #1E40AF !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(17,24,39,0.15) !important;
        }
        div.stButton > button:active {
            transform: translateY(0) !important;
            box-shadow: 0 2px 4px rgba(17,24,39,0.12) !important;
        }
        div[data-testid="stSelectbox"] select {
            font-size: 20px !important;
            padding: 10px !important;
            border: 2px solid #1D4ED8 !important;
            border-radius: 8px !important;
            background-color: #ffffff !important;
            color: #111827 !important;
            width: 100% !important;
        }
        div[data-testid="stSelectbox"] option {
            font-size: 20px !important;
            background-color: #ffffff !important;
            color: #111827 !important;
        }
        div[data-testid="stSelectbox"] option:hover {
            background-color: #1D4ED8 !important;
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Inicializar valores en session_state si no existen
    if "va" not in st.session_state:
        st.session_state.va = 0.0
    if "hce" not in st.session_state:
        st.session_state.hce = 0.0
    if "sce" not in st.session_state:
        st.session_state.sce = 0.0
    if "vaic" not in st.session_state:
        st.session_state.vaic = 0.0
    if "roa" not in st.session_state:
        st.session_state.roa = 0.0
    if "roe" not in st.session_state:
        st.session_state.roe = 0.0
    if "it" not in st.session_state:
        st.session_state.it = 0.0
    if "cv" not in st.session_state:
        st.session_state.cv = 0.0
    if "hc" not in st.session_state:
        st.session_state.hc = 0.0
    if "ce" not in st.session_state:
        st.session_state.ce = 0.0
    if "sector_indicadores" not in st.session_state:
        st.session_state.sector_indicadores = "Inmobiliaria"

    # Selectbox para seleccionar sector
    opciones = ["Inmobiliaria", "Primaria", "Comercial"]
    st.session_state.sector_indicadores = st.selectbox("Selecciona un sector:", opciones)

    # Botón para calcular
    if st.button("Calcular Indicadores", key="btn_calcular"):
        # Obtener valores de entrada
        it = st.session_state.it
        cv = st.session_state.cv
        hc = st.session_state.hc
        ce = st.session_state.ce
        # Cálculos
        va_calculado = it - cv if it >= cv else 0.0
        hce_calculado = va_calculado / hc if hc != 0 else 0.0
        sc = va_calculado - hc if va_calculado >= hc else 0.0
        sce_calculado = sc / va_calculado if va_calculado != 0 else 0.0
        ice_calculado = hce_calculado + sce_calculado
        cee_calculado = va_calculado / ce if ce != 0 else 0.0
        vaic_calculado = ice_calculado + cee_calculado
        # Cálculos de ROA y ROE según el sector
        sector = st.session_state.sector_indicadores
        if sector == "Comercial":
            roa = 0.017000167 + 0.000090463 * ice_calculado + 0.065590993 * cee_calculado
            roe = -0.15508027 + 0.00774242 * ice_calculado + 0.930391243 * cee_calculado
        elif sector == "Primaria":
            roa = 0.027048998 - 0.004791466 * ice_calculado + 0.083361825 * cee_calculado
            roe = 0.084135634 - 0.008724684 * ice_calculado + 0.151617468 * cee_calculado
        else:  # Inmobiliaria
            roa = -0.001171129 + 0.005704393 * ice_calculado + 0.028213145 * cee_calculado
            roe = 0.010838631 + 0.009842492 * ice_calculado + 0.069439342 * cee_calculado

        # Actualizar session_state
        st.session_state.va = va_calculado
        st.session_state.hce = hce_calculado
        st.session_state.sce = sce_calculado
        st.session_state.vaic = vaic_calculado
        st.session_state.roa = roa
        st.session_state.roe = roe

    # Crear 3 columnas con proporción 2:3:3
    col1, col2, col3 = st.columns([2, 3, 3])

    # Columna 2: Entradas base (IT, CV)
    with col2:
        st.session_state.it = st.number_input("Ingresos Totales (IT)", min_value=0.0, value=st.session_state.get("it", 0.0), step=0.01, format="%.2f")
        st.session_state.cv = st.number_input("Costos de Ventas (CV)", min_value=0.0, value=st.session_state.get("cv", 0.0), step=0.01, format="%.2f")
       

    # Columna 3: Entrada base (CE) y (HC)
    with col3:
        st.session_state.hc = st.number_input("Sueldos y Salarios (HC)", min_value=0.0, value=st.session_state.get("hc", 0.0), step=0.01, format="%.2f")
        st.session_state.ce = st.number_input("Activos Netos (CE)", min_value=0.0, value=st.session_state.get("ce", 0.0), step=0.01, format="%.2f")
        
    # Columna 1: Resultados no editables (ROA y ROE)
    with col1:
        st.markdown('<span style="font-weight:bold; font-size:22px; color:#111827;">ROA:</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="readonly" style="font-weight:bold; font-size:22px;margin-left: 1cm;"> {st.session_state.roa:.2f}</div>', unsafe_allow_html=True)
        st.markdown('<span style="font-weight:bold; font-size:22px; color:#111827;">ROE:</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="readonly" style="font-weight:bold; font-size:22px;margin-left: 1cm;"> {st.session_state.roe:.2f}</div>', unsafe_allow_html=True)

    
    # Mostrar resultados adicionales
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="readonly">Valor Añadido (VA): {st.session_state.va:.2f}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="readonly">Índice de Valor Añadido Intelectual (VAIC™): {st.session_state.vaic:.2f}</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown(f'<div class="readonly">Eficiencia Capital Estructural (SCE): {st.session_state.sce:.2f}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="readonly">Eficiencia Capital Humano (HCE): {st.session_state.hce:.2f}</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Recalcular ICE y CEE para el punto (basado en los valores actuales)
    it = st.session_state.it
    cv = st.session_state.cv
    hc = st.session_state.hc
    ce = st.session_state.ce
    va_calculado = it - cv if it >= cv else 0.0
    hce_calculado = va_calculado / hc if hc != 0 else 0.0
    sc = va_calculado - hc if va_calculado >= hc else 0.0
    sce_calculado = sc / va_calculado if va_calculado != 0 else 0.0
    ice_calculado = hce_calculado + sce_calculado
    cee_calculado = va_calculado / ce if ce != 0 else 0.0

    # === GRÁFICAS LIMPIAS: SOLO TUS RESULTADOS (SIN REFERENCIAS) ===
    st.markdown("---")
    st.markdown("### Visualización de Resultados")

   

    # --- Recalcular CEE para usar en gráficos ---
    cee_actual = st.session_state.va / st.session_state.ce if st.session_state.ce != 0 else 0.0

    # --- 1. Radar Chart: Perfil VAIC™ (solo tus valores) ---
    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=[cee_actual, st.session_state.hce, st.session_state.sce, st.session_state.vaic],
        theta=['CEE', 'HCE', 'SCE', 'VAIC™'],
        fill='toself',
        name='Resultados Calculados',
        line_color='#1D4ED8',
        fillcolor='rgba(29, 78, 216, 0.25)'
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(cee_actual, st.session_state.hce, st.session_state.sce, st.session_state.vaic) + 0.5]
            )
        ),
        showlegend=False,
        title="Perfil VAIC™ - Capital Intelectual",
        height=480,
        font=dict(size=14)
    )

    # --- 2. Barras horizontales limpias: ROA y ROE ---
    fig_bar = go.Figure()

    fig_bar.add_trace(go.Bar(
        y=['ROA', 'ROE'],
        x=[st.session_state.roa, st.session_state.roe],
        orientation='h',
        marker_color=['#1D4ED8', '#DC2626'],
        text=[f"{st.session_state.roa:.4f}", f"{st.session_state.roe:.4f}"],
        textposition='outside',
        textfont=dict(size=16, color='#111827'),
        hovertemplate='<b>%{y}</b>: %{x:.4f}<extra></extra>'
    ))

    fig_bar.update_layout(
        title="ROA y ROE Calculados",
        xaxis_title="Valor",
        height=350,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14)
    )

    # --- Mostrar ambas gráficas lado a lado ---
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_radar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- Tabla resumen FINAL (solo tus cálculos, sin referencias) ---
    st.markdown("### Resumen de Indicadores")
    resumen_df = pd.DataFrame({
        "Indicador": ["Valor Añadido (VA)", "Eficiencia Capital Humano (HCE)", 
                      "Eficiencia Capital Estructural (SCE)", "Eficiencia Capital Empleado (CEE)", 
                      "VAIC™", "ROA", "ROE"],
        "Valor Calculado": [
            f"{st.session_state.va:,.2f}",
            f"{st.session_state.hce:.4f}",
            f"{st.session_state.sce:.4f}",
            f"{cee_actual:.4f}",
            f"{st.session_state.vaic:.4f}",
            f"{st.session_state.roa:.4f}",
            f"{st.session_state.roe:.4f}"
        ]
    })

    st.dataframe(
        resumen_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Indicador": st.column_config.Column(width="medium"),
            "Valor Calculado": st.column_config.Column(width="medium")
        }
    )
    
    
def mostrar_exportacion():
    st.title("Exportar resultados en PDF")

    # CSS para botón bonito
    st.markdown("""
    <style>
        div.stButton > button {
            font-size: 20px !important; padding: 12px !important; background-color: #1D4ED8 !important;
            color: white !important; border: 2px solid #1E3A8A !important; border-radius: 10px !important;
            font-weight: bold !important;
        }
        div.stButton > button:hover {
            background-color: #1E40AF !important; transform: translateY(-3px) !important;
            box-shadow: 0 8px 20px rgba(29, 78, 216, 0.3) !important;
        }
    </style>
    """, unsafe_allow_html=True)

    if st.session_state.va == 0.0:
        st.warning("Por favor, calcula los indicadores primero en la página de Indicadores.")
        return

    # Mostrar resumen rápido
    st.markdown("### Resultados Calculados")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**VA:** {st.session_state.va:,.2f}")
        st.markdown(f"**HCE:** {st.session_state.hce:.4f}")
        st.markdown(f"**SCE:** {st.session_state.sce:.4f}")
    with col2:
        st.markdown(f"**VAIC™:** {st.session_state.vaic:.4f}")
        st.markdown(f"**ROA:** {st.session_state.roa:.4f}")
        st.markdown(f"**ROE:** {st.session_state.roe:.4f}")

    if st.button("Generar PDF", use_container_width=True):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # === ENCABEZADO PROFESIONAL ===
        c.setFillColorRGB(120/255, 31/255, 25/255)  # Rojo UTA
        c.rect(0, height - 100, width, 100, fill=1)
        
        try:
            logo = Image.open("UTA.png")
            logo_width = 80
            c.drawImage("UTA.png", 50, height - 110, width=logo_width, preserveAspectRatio=True)
        except:
            pass  # Si no encuentra la imagen, sigue sin ella

        c.setFillColorRGB(1, 1, 1)  # Blanco
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width / 2, height - 60, " INDICADORES INTANGIBLES")
        c.setFont("Helvetica", 14)
        c.drawCentredString(width / 2, height - 85, "Universidad Técnica de Ambato | Ecuador")

        # Línea decorativa
        c.setStrokeColorRGB(0.9, 0.9, 0.9)
        c.setLineWidth(3)
        c.line(50, height - 105, width - 50, height - 105)

        # === CONTENIDO ===
        y = height - 140
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(70, y, "Resultados del Análisis VAIC™ y Rentabilidad")
        y -= 30

        c.setFont("Helvetica", 12)
        c.drawString(70, y, f"Sector seleccionado: {st.session_state.sector_indicadores}")
        y -= 25
        from datetime import datetime
        c.drawString(70, y, f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        y -= 40

        # === TABLA DE RESULTADOS ===
        c.setFont("Helvetica-Bold", 12)
        c.drawString(70, y, "Indicadores Calculados:")
        y -= 20

        datos = [
            ["Valor Añadido (VA)", f"${st.session_state.va:,.2f}"],
            ["Eficiencia Capital Humano (HCE)", f"{st.session_state.hce:.4f}"],
            ["Eficiencia Capital Estructural (SCE)", f"{st.session_state.sce:.4f}"],
            ["Eficiencia Capital Empleado (CEE)", f"{(st.session_state.va / st.session_state.ce if st.session_state.ce != 0 else 0):.4f}"],
            ["VAIC™", f"{st.session_state.vaic:.4f}"],
            ["ROA", f"{st.session_state.roa:.4f}"],
            ["ROE", f"{st.session_state.roe:.4f}"]
        ]

        c.setFont("Helvetica", 11)
        for label, valor in datos:
            c.drawString(90, y, f"• {label}:")
            c.setFont("Helvetica-Bold", 11)
            c.drawString(300, y, valor)
            c.setFont("Helvetica", 11)
            y -= 20

        y -= 30

        # === GRÁFICAS EN EL PDF ===
        try:
            # Recalcular CEE
            cee_actual = st.session_state.va / st.session_state.ce if st.session_state.ce != 0 else 0.0

            # 1. Radar Chart
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=[cee_actual, st.session_state.hce, st.session_state.sce, st.session_state.vaic],
                theta=['CEE', 'HCE', 'SCE', 'VAIC™'],
                fill='toself',
                line_color="#D8491D",
                fillcolor='rgba(29, 78, 216, 0.25)'
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                showlegend=False,
                title="Perfil VAIC™ - Capital Intelectual",
                height=400, width=550
            )
            radar_img = io.BytesIO()
            fig_radar.write_image(radar_img, format="png")
            radar_img.seek(0)
            c.drawImage(radar_img, 40, y - 320, width=500, height=300)

            # 2. Barras ROA y ROE
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                y=['ROA', 'ROE'],
                x=[st.session_state.roa, st.session_state.roe],
                orientation='h',
                marker_color=['#1D4ED8', '#DC2626'],
                text=[f"{st.session_state.roa:.4f}", f"{st.session_state.roe:.4f}"],
                textposition='outside'
            ))
            fig_bar.update_layout(
                title="ROA y ROE Calculados",
                height=300, width=500,
                margin=dict(l=50, r=50, t=50, b=50)
            )
            bar_img = io.BytesIO()
            fig_bar.write_image(bar_img, format="png")
            bar_img.seek(0)
            c.drawImage(bar_img, 40, y - 650, width=500, height=250)

        except Exception as e:
            c.setFont("Helvetica", 10)
            c.drawString(70, y - 400, f"Advertencia: No se pudieron generar las gráficas: {str(e)}")

        # === PIE DE PÁGINA ===
        c.setFillColorRGB(120/255, 31/255, 25/255)
        c.rect(0, 0, width, 70, fill=1)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width / 2, 35, "Proyecto de Investigación - Universidad Técnica de Ambato")
        

        c.save()
        buffer.seek(0)

        st.success("¡PDF generado con éxito!")
        st.download_button(
            label="Descargar Reporte Completo (PDF)",
            data=buffer,
            file_name=f"Reporte_VAIC_{st.session_state.sector_indicadores}_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )



def mostrar_ayuda():
   
    # ------------------------------
    # Minimal CSS styling
    # ------------------------------
    st.markdown(
        """
        <style>
        .title {font-size: 2.0rem; font-weight: 800; margin-bottom: 0.25rem; color:#111827;}
        .subtitle {font-size: 1.05rem; color: #475569; margin-top: -0.25rem; margin-bottom: 1rem;}
        .card {background: #ffffff; border: 1px solid #E5E7EB; border-radius: 16px; padding: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);}
        .kpi {font-size: 0.9rem; font-weight: 600; color: #111827;}
        .formula {font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; background:#F8FAFC; border-radius: 10px; padding: 10px; border: 1px solid #E5E7EB; color:#0f172a;}
        .pill {display: inline-block; padding: 4px 10px; border-radius: 999px; font-size: 0.78rem; font-weight: 600; border: 1px solid #E5E7EB; background: #F8FAFC; margin-right: 6px; margin-top:6px; color:#0f172a;}
        .muted {color: #64748b; font-size: 0.92rem;}
        .section-title {font-size: 1.2rem; font-weight: 800; margin-bottom: 0.4rem; margin-top: 0.6rem; color:#111827;}
        </style>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------
    # Sidebar Navigation
    # ------------------------------
    with st.sidebar:
        st.image("UTA.png", caption="Material de apoyo", use_column_width=True)
        st.markdown("### Navegación")
        section = st.radio(
            "Ir a:",
            ["Resumen", "Glosario y Fórmulas", "Relación con ROA & ROE", "Notas"],
            index=0
        )
        st.markdown("---")
        st.markdown("**Consejo:** usa ☑️ expanders para estudio rápido.")
        st.caption("Autor: Alex Mantilla")

    # ------------------------------
    # Header
    # ------------------------------
    st.markdown('<div class="title">📘 Hoja de ayuda: Capital intelectual, VAIC™, ROA y ROE</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Guía rápida para docentes y estudiantes — sin resultados econométricos, solo lógica conceptual.</div>', unsafe_allow_html=True)

    # ------------------------------
    # Helper components
    # ------------------------------
    def pill(text):
        st.markdown(f'<span class="pill">{text}</span>', unsafe_allow_html=True)

    def formula(text):
        st.markdown(f'<div class="formula">{text}</div>', unsafe_allow_html=True)

    # ------------------------------
    # Sections
    # ------------------------------
    if section == "Resumen":
        with st.container():
            st.markdown('---')
            st.markdown('<div class="section-title">🧭 Objetivo de la hoja</div>', unsafe_allow_html=True)
            st.write(
                "Entender los componentes del modelo **VAIC™** (CEE, HCE, SCE), sus definiciones, "
                "fórmulas y cómo, en términos conceptuales, contribuyen al **ROA** y al **ROE**."
            )
            st.markdown('<div class="section-title">🔎 Idea central</div>', unsafe_allow_html=True)
            st.write(
                "El **valor añadido (VA)** creado por la empresa es distribuido entre **capital humano (HC)**, "
                "**capital estructural (SC)** y **capital empleado (CE)**. El **VAIC™ = CEE + HCE + SCE** resume "
                "qué tan eficientemente los recursos tangibles e intangibles se convierten en valor económico."
            )
            st.markdown('<div class="section-title">🏷️ Etiquetas clave</div>', unsafe_allow_html=True)
            cols = st.columns(6)
            with cols[0]: pill("VA")
            with cols[1]: pill("HC")
            with cols[2]: pill("SC")
            with cols[3]: pill("CE")
            with cols[4]: pill("CEE")
            with cols[5]: pill("HCE / SCE")
            st.markdown('---')

    elif section == "Glosario y Fórmulas":
        st.markdown('---')
        st.markdown('<div class="section-title">📚 Glosario básico</div>', unsafe_allow_html=True)
        with st.expander("Valor Añadido (VA)"):
            st.write("**Definición:** Riqueza creada por la empresa.")
            formula("VA = Ingresos Totales – Costos de Ventas")
        with st.expander("Capital Humano (HC)"):
            st.write("**Definición:** Inversión en personas (sueldos y salarios).")
        with st.expander("Capital Estructural (SC)"):
            st.write("**Definición:** Procesos, patentes, sistemas, cultura organizativa, etc.")
            formula("SC = VA – HC")
        with st.expander("Capital Empleado (CE)"):
            st.write("**Definición:** Activos netos en libros (inversión efectiva para producir).")
        st.markdown('<div class="section-title">🧮 Indicadores VAIC™</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**CEE**")
            formula("CEE = VA / CE")
            st.caption("Eficiencia del uso de activos.")
        with c2:
            st.markdown("**HCE**")
            formula("HCE = VA / HC")
            st.caption("Eficiencia del capital humano.")
        with c3:
            st.markdown("**SCE**")
            formula("SCE = SC / VA")
            st.caption("Eficiencia del capital estructural.")
        st.markdown("**VAIC™ agregado**")
        formula("VAIC™ = CEE + HCE + SCE")
        st.markdown('<div class="section-title">📊 Rentabilidad</div>', unsafe_allow_html=True)
        c4, c5 = st.columns(2)
        with c4:
            st.markdown("**ROA**")
            formula("ROA = Utilidad Neta / Activo Total")
        with c5:
            st.markdown("**ROE**")
            formula("ROE = Utilidad Neta / Patrimonio")
        st.markdown("</div>", unsafe_allow_html=True)

    elif section == "Relación con ROA & ROE":
        st.markdown('---')
        st.markdown('<div class="section-title">🧩 Lógica conceptual de influencia</div>', unsafe_allow_html=True)
        st.markdown("**CEE → ROA / ROE**")
        st.write("- Uso eficiente de activos (CE) para generar VA. Mejor CEE suele elevar **ROA** y **ROE**.")
        st.markdown("**HCE → ROA / ROE**")
        st.write("- Productividad e innovación del talento elevan VA; impulsa **ROA** y, sostenidamente, **ROE**.")
        st.markdown("**SCE → ROA / ROE**")
        st.write("- Procesos y sistemas que hacen repetible el desempeño; protege **ROA** y estabiliza **ROE**.")
        st.markdown("**VAIC™ → ROA / ROE**")
        st.write("- Suma integrada de eficiencias; mayor capacidad de transformar recursos en valor económico.")
        st.info("Nota: Esta sección explica relaciones conceptuales, no resultados de regresión.")
        st.markdown('---')

   
    elif section == "Notas":
        st.markdown('---')
        st.markdown('<div class="section-title">🗒️ Notas y referencias internas</div>', unsafe_allow_html=True)
        st.write(
            "Definiciones y fórmulas basadas en la literatura de **Pulic (2000, 2004)** y "
            "resúmenes académicos que calculan **CEE, HCE, SCE y VAIC™** a partir de estados financieros. "
            "Esta herramienta es didáctica y evita reportar resultados econométricos; "
            "su foco es conceptual."
        )
    st.markdown('---')




def main():
    aplicar_animaciones_css()  # <-- NUEVO: solo agrega animaciones (no cambia lógica)
    # CSS corporativo para botones (manteniendo tamaños/estructura que ya tenías)
    st.markdown("""
    <style>
        /* Botones con paleta empresarial */
        div.stButton > button {
            font-size: 50px !important;
            height: 80px !important;
            padding: 15px 20px !important;
            font-weight: bold !important;
            border-radius: 12px !important;
            border: 2px solid #1E3A8A !important;  /* azul-800 */
            background-color: #1D4ED8 !important;   /* azul-600 */
            color: #ffffff !important;
            transition: all 0.3s ease !important;
        }
        
        div.stButton > button:hover {
            background-color: #1E40AF !important;   /* azul-700 */
            color: #ffffff !important;
            border-color: #1E40AF !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(17,24,39,0.15) !important;
        }
        
        div.stButton > button:active {
            transform: translateY(0) !important;
            box-shadow: 0 2px 4px rgba(17,24,39,0.12) !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Resto del código igual
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🏠 Inicio", use_container_width=True, key="btn_inicio"):
            cambiar_pagina("inicio")

    with col2:
        if st.button("📊 Indicadores", use_container_width=True, key="btn_indicadores"):
            cambiar_pagina("indicadores")

    with col3:
        if st.button("📤 Exportar", use_container_width=True, key="btn_exportar"):
            cambiar_pagina("exportar")
    
    with col4:
        if st.button("🆘 Ayuda", use_container_width=True, key="btn_ayuda"):
            cambiar_pagina("ayuda")
                  
    st.markdown("---")
    if st.session_state.pagina == "inicio":
        mostrar_inicio()
    elif st.session_state.pagina == "indicadores":
        mostrar_indicadores()
    elif st.session_state.pagina == "exportar":
        mostrar_exportacion()
    elif st.session_state.pagina == "ayuda":
        mostrar_ayuda()

st.markdown("""
    <style>
    .stApp {
        background-color: #F5F7FB; /* fondo claro corporativo */
    }
    </style>
""", unsafe_allow_html=True)    

if __name__ == '__main__':
    main()