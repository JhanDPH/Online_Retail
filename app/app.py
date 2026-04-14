import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Retail Dashboard", layout="wide")

# =========================
# ESTILO (CSS PRO)
# =========================
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
h1, h2, h3 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# CARGA DE DATOS
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv('data/online_retail.csv', encoding='ISO-8859-1')
    
    df = df.dropna(subset=['CustomerID'])
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] > 0]

    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    
    return df

df = load_data()

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🔎 Filtros")

countries = st.sidebar.multiselect(
    "País",
    options=sorted(df['Country'].unique()),
    default=sorted(df['Country'].unique())
)

df = df[df['Country'].isin(countries)]

# =========================
# TITULO
# =========================
st.title("📊 Panel de Comercio Online")

# =========================
# KPIs
# =========================
total_sales = df['TotalPrice'].sum()
total_orders = df['InvoiceNo'].nunique()
total_customers = df['CustomerID'].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Ventas Totales", f"${total_sales:,.0f}")
col2.metric("🧾 Órdenes", f"{total_orders:,}")
col3.metric("👤 Clientes", f"{total_customers:,}")

# =========================
# VENTAS MENSUALES
# =========================
st.subheader("📈 Ventas Mensuales")

monthly_sales = df.set_index('InvoiceDate')['TotalPrice'].resample('ME').sum()

fig1 = px.line(
    monthly_sales,
    x=monthly_sales.index,
    y=monthly_sales.values,
    title="Evolución de Ventas",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# TOP PRODUCTOS
# =========================
st.subheader("🛍️ Top Productos")

top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)

fig2 = px.bar(
    top_products,
    x=top_products.values,
    y=top_products.index,
    orientation='h',
    title="Top 10 Productos"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# VENTAS POR PAÍS
# =========================
st.subheader("🌍 Ventas por País")

country_sales = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(10)

fig3 = px.bar(
    country_sales,
    x=country_sales.index,
    y=country_sales.values,
    title="Top Países"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# RFM
# =========================
st.subheader("👤 Segmentación de Clientes (RFM)")

snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'count',
    'TotalPrice': 'sum'
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']

# Scores
rfm['R_score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1]).astype(int)
rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5]).astype(int)
rfm['M_score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5]).astype(int)

# Score combinado
rfm['RFM_Score'] = (
    rfm['R_score'].astype(str) +
    rfm['F_score'].astype(str) +
    rfm['M_score'].astype(str)
)

# Segmentación
def segment_customer(row):
    if row['RFM_Score'] == '555':
        return 'VIP'
    elif row['R_score'] >= 4:
        return 'Loyal'
    elif row['R_score'] == 1:
        return 'Lost'
    else:
        return 'Regular'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

import plotly.express as px

segment_counts = rfm['Segment'].value_counts().reset_index()
segment_counts.columns = ['Segment', 'Count']

col1, col2 = st.columns([1,6])  # 👈 más espacio al gráfico

with col2:
    fig = px.pie(
        segment_counts,
        names='Segment',
        values='Count',
        hole=0.5,
        color='Segment',
        color_discrete_map={
            'VIP': '#08306B',
            'Loyal': '#2171B5',
            'Regular': '#6BAED6',
            'Lost': '#C6DBEF'
        }
    )

    fig.update_layout(
        height=450,  # 👈 tamaño más grande
        showlegend=True
    )

st.plotly_chart(fig, use_container_width=True)

# =========================
# 🌍 MAPA SEGMENTACIÓN PARETO (CORREGIDO)
# =========================

import pandas as pd
import plotly.express as px

st.subheader("🌍 Segmentación Estratégica de Países")

# =========================
# 1. AGRUPAR DATOS
# =========================

country_sales = df.groupby('Country')['TotalPrice'].sum().reset_index()

# =========================
# 2. ORDENAR
# =========================

country_sales = country_sales.sort_values(by='TotalPrice', ascending=False)

# =========================
# 3. PARETO (% ACUMULADO)
# =========================

country_sales['Perc'] = country_sales['TotalPrice'] / country_sales['TotalPrice'].sum()
country_sales['Perc_Acum'] = country_sales['Perc'].cumsum()

# =========================
# 4. SEGMENTACIÓN
# =========================

def classify_country(x):
    if x <= 0.5:
        return 'Top'
    elif x <= 0.75:
        return 'High'
    elif x <= 0.9:
        return 'Medium'
    else:
        return 'Low'

country_sales['Segment'] = country_sales['Perc_Acum'].apply(classify_country)

# =========================
# 5. LIMPIEZA (🔥 CLAVE)
# =========================

country_sales['Segment'] = country_sales['Segment'].astype(str).str.strip()

# =========================
# 6. FORZAR CATEGORÍAS (🔥 EVITA ERROR DE COLORES)
# =========================

country_sales['Segment'] = pd.Categorical(
    country_sales['Segment'],
    categories=['Top', 'High', 'Medium', 'Low'],
    ordered=True
)

# =========================
# 7. MAPA DE COLORES (CONSISTENTE)
# =========================

color_map = {
    'Top': '#08306B',     # azul fuerte
    'High': '#2171B5',    # azul medio fuerte
    'Medium': '#6BAED6',  # azul medio
    'Low': '#C6DBEF'      # azul claro
}

# =========================
# 8. CREAR MAPA
# =========================

fig_map = px.choropleth(
    country_sales,
    locations='Country',
    locationmode='country names',
    color='Segment',
    color_discrete_map=color_map,
    title='Segmentación Estratégica de Países (Pareto)'
)

# =========================
# 9. ESTILO PRO
# =========================

fig_map.update_layout(
    height=700,
    margin=dict(l=0, r=0, t=50, b=0),
    geo=dict(bgcolor='black'),
    paper_bgcolor='black',
    plot_bgcolor='black'
)

fig_map.update_geos(
    showcountries=True,
    showcoastlines=True,
    showland=True
)

# =========================
# 10. MOSTRAR
# =========================

st.plotly_chart(fig_map, use_container_width=True)