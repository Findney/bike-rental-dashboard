import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime

# Load dataset
day_df = pd.read_csv('data/day.csv')
hour_df = pd.read_csv('data/hour.csv')
rfm_df = pd.read_csv('data/rfm_analysis.csv')

# Konversi kolom tanggal ke format datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Gabungkan dataset berdasarkan tanggal
df = pd.merge(hour_df, day_df[['dteday', 'season', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'hum', 'windspeed']], 
              on='dteday', how='left', suffixes=('', '_day'))

# Konfigurasi Streamlit
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("🚲 Bike Sharing Dashboard")

with st.sidebar:
    # Menampilkan logo perusahaan
    st.image("https://raw.githubusercontent.com/Findney/dataset/refs/heads/main/images/bike.png")
    
    # Sidebar untuk memilih rentang tanggal
    st.header("Pilih Rentang Tanggal")
    date_range = st.date_input(
        "Pilih tanggal awal dan akhir",
        (df['dteday'].min(), df['dteday'].max())  # Default: seluruh rentang data
    )

# Pastikan pengguna memilih dua tanggal
if len(date_range) == 2:
    start_date, end_date = date_range
    df_filtered = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]
    
    st.write(f"Menampilkan data dari **{start_date}** hingga **{end_date}**")
    
    # Statistik Umum
    st.subheader("📊 Statistik Umum")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Penyewaan", f"{df_filtered['cnt'].sum():,}")
    col2.metric("Rata-rata Penyewaan Harian", f"{df_filtered['cnt'].mean():.2f}")
    col3.metric("Total Hari dalam Data", f"{df_filtered['dteday'].nunique()} hari")

    # Analisis Pola Penyewaan
    st.subheader("📊 Analisis Pola Penyewaan Sepeda")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Pola Penyewaan Berdasarkan Jam")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.lineplot(data=df_filtered.groupby('hr')['cnt'].mean(), marker="o")
        plt.xlabel("Jam")
        plt.ylabel("Jumlah Penyewaan")
        plt.title("Rata-rata Penyewaan Sepeda Berdasarkan Jam")
        plt.xticks(range(0, 24))
        plt.grid(True)
        st.pyplot(fig)

    with col2:
        st.markdown("##### Pengaruh Cuaca terhadap Penyewaan")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x='weathersit', y='cnt', data=day_df, hue='weathersit', palette='Set2', errorbar=None, legend=False)
        plt.xlabel("Kondisi Cuaca (1=Baik, 2=Mendung, 3=Hujan)")
        plt.ylabel("Jumlah Penyewaan")
        plt.title("Distribusi Penyewaan Sepeda Berdasarkan Cuaca")
        st.pyplot(fig)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Penyewaan Sepeda Berdasarkan Hari")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x='weekday', y='cnt', data=day_df, hue='weekday', palette='Set2', errorbar=None, legend=False)
        plt.xlabel("Hari (0=Minggu, 6=Sabtu)")
        plt.ylabel("Jumlah Penyewaan")
        plt.title("Distribusi Penyewaan Sepeda Berdasarkan Hari")
        st.pyplot(fig)
    
    with col2:
        # Pola Penyewaan antara Hari Kerja & Akhir Pekan
        st.markdown("##### Penyewaan antara Hari Kerja & Akhir Pekan")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(data=df_filtered, x='workingday', y='cnt', palette=['red', 'blue'], hue='workingday', errorbar=None, legend=False)
        plt.xticks([0, 1], ["Akhir Pekan", "Hari Kerja"])
        plt.xlabel("Kategori Hari")
        plt.ylabel("Jumlah Penyewaan")
        plt.title("Distribusi Penyewaan Sepeda pada Hari Kerja vs Akhir Pekan")
        st.pyplot(fig)
    
    

    # Analisis RFM
    st.subheader("🔍 Analisis RFM")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Distribusi Segmen Pelanggan")
        fig, ax = plt.subplots(figsize=(6, 5.3))
        rfm_df['Segment'].value_counts().plot.pie(autopct='%1.1f%%', colors=['gold', 'skyblue', 'lightcoral', 'lightgreen'])
        plt.ylabel('')
        st.pyplot(fig)

    with col2:
        st.markdown("##### Scatter Plot Recency vs Frequency")
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.scatterplot(data=rfm_df, x='Recency', y='Frequency', hue='Segment', palette='viridis', alpha=0.7)
        plt.xlabel("Recency")
        plt.ylabel("Frequency")
        st.pyplot(fig)

    # Unduh Data yang Telah Difilter
    st.subheader("📥 Unduh Data yang Telah Difilter")
    st.download_button(
        label="Download Data",
        data=df_filtered.to_csv(index=False).encode('utf-8'),
        file_name="filtered_data.csv",
        mime="text/csv"
    )
else:
    st.warning("Silakan pilih dua tanggal untuk menampilkan visualisasi!")

st.caption('Copyright © Agil Mughni 2025')
