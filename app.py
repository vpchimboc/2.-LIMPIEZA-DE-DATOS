import mysql.connector
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

# =========================
# CONFIGURACIÓN
# =========================
st.set_page_config(page_title="Dashboard Big Data", layout="wide")

st.title("📊 Dashboard Estilo Power BI - Big Data")

# =========================
# CONEXIÓN MYSQL
# =========================
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bd_lavadora"
)

df_base = pd.read_sql("SELECT * FROM cliente", con=conexion)

df = df_base.copy()

# =========================
# MENÚ LATERAL (POWER BI STYLE)
# =========================
menu = st.sidebar.selectbox(
    "📌 Menú de Navegación",
    [
        "📂 Exploración de Datos",
        "🧹 Limpieza de Datos",
        "🔄 Transformación de Datos",
        "📊 Visualización",
        "📦 Dataset Final",
        "⬇️ Exportar Datos"
    ]
)

# =========================================================
# 📂 EXPLORACIÓN DE DATOS
# =========================================================
if menu == "📂 Exploración de Datos":

    st.header("Exploración de Datos")

    st.dataframe(df)

    st.subheader("Primeras filas")
    st.dataframe(df.head())

    st.subheader("Últimas filas")
    st.dataframe(df.tail())

    st.subheader("Info del DataFrame")

    buffer = io.StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())

    st.subheader("Estadísticas")
    st.dataframe(df.describe())

    st.subheader("Valores nulos")
    st.write(df.isnull().sum())

    st.subheader("Duplicados")
    st.write(df.duplicated().sum())

    st.subheader("Tipos de datos")
    st.dataframe(df.dtypes)

# =========================================================
# 🧹 LIMPIEZA DE DATOS
# =========================================================
elif menu == "🧹 Limpieza de Datos":

    st.header("Limpieza de Datos")

    st.subheader("Eliminar nulos")
    df = df.dropna()
    st.dataframe(df)

    st.subheader("Reemplazar nulos (media)")
    df = df.fillna(df.mean(numeric_only=True))
    st.dataframe(df)

    st.subheader("Eliminar duplicados")
    df = df.drop_duplicates()
    st.dataframe(df)

# =========================================================
# 🔄 TRANSFORMACIÓN DE DATOS
# =========================================================
elif menu == "🔄 Transformación de Datos":

    st.header("Transformación de Datos")

    # ------------------------
    # variable simulada ventas
    # ------------------------
    np.random.seed(42)
    df["ventas"] = np.random.randint(100, 1000, len(df))

    st.subheader("Dataset con ventas")
    st.dataframe(df)

    # ------------------------
    # Normalización
    # ------------------------
    df["ventas_norm"] = (
        (df["ventas"] - df["ventas"].min()) /
        (df["ventas"].max() - df["ventas"].min())
    )

    # ------------------------
    # Z-score
    # ------------------------
    df["ventas_z"] = (
        (df["ventas"] - df["ventas"].mean()) / df["ventas"].std()
    )

    # ------------------------
    # Log
    # ------------------------
    df["ventas_log"] = np.log1p(df["ventas"])

    # ------------------------
    # Binning
    # ------------------------
    df["categoria"] = pd.cut(
        df["ventas"],
        bins=[0, 300, 600, 1000],
        labels=["Bajo", "Medio", "Alto"]
    )

    st.subheader("Datos transformados")
    st.dataframe(df)

# =========================================================
# 📊 VISUALIZACIÓN (DASHBOARD POWER BI STYLE)
# =========================================================
elif menu == "📊 Visualización":

    st.header("Visualización de Datos")

    np.random.seed(42)
    df["ventas"] = np.random.randint(100, 1000, len(df))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribución")
        fig, ax = plt.subplots()
        ax.hist(df["ventas"], bins=10)
        st.pyplot(fig)

    with col2:
        st.subheader("Outliers")
        fig, ax = plt.subplots()
        sns.boxplot(x=df["ventas"], ax=ax)
        st.pyplot(fig)

    st.subheader("Relación de datos")
    st.dataframe(df[["ventas"]])

# =========================================================
# 📦 DATASET FINAL
# =========================================================
elif menu == "📦 Dataset Final":

    st.header("Dataset Final Procesado")

    np.random.seed(42)
    df["ventas"] = np.random.randint(100, 1000, len(df))

    df["ventas_norm"] = (
        (df["ventas"] - df["ventas"].min()) /
        (df["ventas"].max() - df["ventas"].min())
    )

    df["ventas_z"] = (
        (df["ventas"] - df["ventas"].mean()) / df["ventas"].std()
    )

    df["ventas_log"] = np.log1p(df["ventas"])

    df["categoria"] = pd.cut(
        df["ventas"],
        bins=[0, 300, 600, 1000],
        labels=["Bajo", "Medio", "Alto"]
    )

    st.dataframe(df)

    st.subheader("Estadísticas finales")
    st.dataframe(df.describe())

# =========================================================
# ⬇️ EXPORTAR DATOS
# =========================================================
elif menu == "⬇️ Exportar Datos":

    st.header("Descarga de Datos Limpios")

    np.random.seed(42)
    df["ventas"] = np.random.randint(100, 1000, len(df))

    df["ventas_norm"] = (
        (df["ventas"] - df["ventas"].min()) /
        (df["ventas"].max() - df["ventas"].min())
    )

    df["ventas_z"] = (
        (df["ventas"] - df["ventas"].mean()) / df["ventas"].std()
    )

    df["ventas_log"] = np.log1p(df["ventas"])

    df["categoria"] = pd.cut(
        df["ventas"],
        bins=[0, 300, 600, 1000],
        labels=["Bajo", "Medio", "Alto"]
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Descargar CSV",
        data=csv,
        file_name="datos_transformados.csv",
        mime="text/csv"
    )