# 🛒 Online Retail Analysis Project

## 📌 Descripción

Este proyecto tiene como objetivo analizar el comportamiento de ventas de un negocio de retail online utilizando técnicas de análisis de datos para identificar patrones, tendencias y oportunidades de mejora en el negocio.

El análisis se basa en un dataset real que contiene información sobre transacciones, productos, clientes y países.

---

## 🎯 Objetivos del Proyecto

* Analizar la evolución de las ventas en el tiempo
* Identificar los países con mayor generación de ingresos
* Detectar los productos más vendidos
* Segmentar clientes según su comportamiento (RFM)
* Generar insights estratégicos para el negocio

---

## 🗂️ Estructura del Proyecto

```
online_retail_project/
│
├── data/              # Dataset original
├── notebooks/         # Análisis exploratorio (EDA)
├── images/            # Gráficas generadas
├── reports/           # Reporte final de análisis
├── app/               # Dashboard en Streamlit
├── src/               # Funciones reutilizables
├── README.md
└── environment.yml
```

---

## 🛠️ Tecnologías Utilizadas

* Python 🐍
* Pandas
* NumPy
* Matplotlib / Seaborn
* Plotly
* Streamlit

---

## 📊 Dashboard Interactivo

El proyecto incluye un dashboard interactivo desarrollado en Streamlit que permite explorar:

* 📈 Tendencia de ventas
* 🌍 Segmentación de países
* 👤 Segmentación de clientes (RFM)
* 📦 Productos más vendidos

imagenes/Dashboard_interactivo.png

### ▶️ Ejecutar el dashboard

```bash
streamlit run app/app.py
```

```link
http://localhost:8501
```

---

## 💡 Insights Principales

* Reino Unido concentra la mayor parte de los ingresos
* Un pequeño grupo de clientes genera la mayor parte de las ventas (principio de Pareto)
* Existen clientes VIP con alto valor económico
* Algunos países presentan bajo impacto comercial
* Las ventas presentan patrones temporales claros

---

## 🚀 Recomendaciones de Negocio

* Enfocar estrategias en clientes VIP y leales
* Optimizar inventario de productos más vendidos
* Expandir presencia en países con potencial de crecimiento
* Implementar campañas en períodos de alta demanda
* Diseñar estrategias de retención para clientes perdidos

---

## 📄 Reporte

El análisis detallado se encuentra en la carpeta:

```
reports/Analisis_Ventas
```

Incluye:

* Análisis exploratorio
* Segmentación RFM
* Segmentación de países
* Conclusiones estratégicas

---

## 🎯 Resultados del Proyecto

Este proyecto permitió:

* Identificar mercados clave
* Detectar clientes de alto valor
* Analizar patrones de compra
* Apoyar la toma de decisiones basada en datos

👨‍💻 Autor

Jhan Daniel Parra

---

## ⭐ Nota Final

Este proyecto forma parte de mi portafolio de análisis de datos y demuestra habilidades en:

* Análisis exploratorio de datos
* Visualización
* Segmentación de clientes
* Desarrollo de dashboards

---

## ▶️ Cómo ejecutar el proyecto

1. Clonar el repositorio:

```bash
git clone https://github.com/tu-usuario/online_retail_project.git

# Instalar Dependencias : 

conda env create -f environment.yml
conda activate online_retail

# Ejecutar el Notebook:
jupyter notebook

🤝 Contribuciones

- Las contribuciones son bienvenidas 🙌

- Si deseas mejorar este proyecto:

- 1 Haz un fork del repositorio
- 2 Crea una nueva rama (feature/nueva-mejora)
- 3 Realiza tus cambios
- 4 Envía un pull request

📌 Próximas mejoras

- Segmentación de clientes (RFM)
- Dashboard interactivo
- Modelos de predicción de ventas