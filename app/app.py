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
    df = pd.read_csv('../data/online_retail.csv', encoding='ISO-8859-1')
    
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