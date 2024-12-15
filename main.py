import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Dataset URL
url = "https://raw.githubusercontent.com/marceloreis/HTI/master/PRSA_Data_20130301-20170228/PRSA_Data_Aotizhongxin_20130301-20170228.csv"
data = pd.read_csv(url)

# Data Cleaning
data = data.dropna()  # Menghapus nilai NaN
data['date'] = pd.to_datetime(data[['year', 'month', 'day']])
data['hour'] = data['hour']

# Sidebar
st.sidebar.title("Filter Data")
st.sidebar.markdown("### Pilih Rentang Waktu")
min_date = data['date'].min()
max_date = data['date'].max()
start_date, end_date = st.sidebar.date_input(
    label="Rentang Tanggal", value=(min_date, max_date), min_value=min_date, max_value=max_date
)

# Filter dataset berdasarkan tanggal
filtered_data = data[(data['date'] >= pd.to_datetime(start_date)) & (data['date'] <= pd.to_datetime(end_date))]

# Pertanyaan 1: Tren rata-rata PM2.5 per bulan
filtered_data['month'] = filtered_data['date'].dt.to_period("M")
monthly_avg_pm25 = filtered_data.groupby('month')['PM2.5'].mean().reset_index()

# Pertanyaan 2: Korelasi antar faktor
correlation_matrix = filtered_data[['PM2.5', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()

# Pertanyaan 3: Distribusi nilai PM2.5
distribution_pm25 = filtered_data['PM2.5']

# Pertanyaan 4: Rata-rata PM2.5 berdasarkan jam
hourly_avg_pm25 = filtered_data.groupby('hour')['PM2.5'].mean().reset_index()

# Dashboard Utama
st.title("Dashboard Analisis PM2.5")
st.markdown("### Menjelajahi Tren dan Korelasi Faktor yang Mempengaruhi Polusi Udara")

# Statistik Ringkas
col1, col2 = st.columns(2)

with col1:
    avg_pm25 = filtered_data['PM2.5'].mean()
    st.metric(label="Rata-rata PM2.5", value=f"{avg_pm25:.2f}")

with col2:
    total_data_points = len(filtered_data)
    st.metric(label="Jumlah Data", value=total_data_points)

# Visualisasi 1: Tren rata-rata PM2.5 per bulan
st.subheader("Tren Rata-rata PM2.5 per Bulan")
plt.figure(figsize=(10, 6))
plt.plot(monthly_avg_pm25['month'].astype(str), monthly_avg_pm25['PM2.5'], marker='o', color='blue')
plt.xticks(rotation=45)
plt.title("Rata-rata PM2.5 per Bulan")
plt.xlabel("Bulan")
plt.ylabel("Rata-rata PM2.5")
st.pyplot(plt.gcf())

# Visualisasi 2: Korelasi antar faktor
st.subheader("Korelasi Antar Variabel")
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
st.pyplot(plt.gcf())

# Visualisasi 3: Distribusi PM2.5
st.subheader("Distribusi Nilai PM2.5")
plt.figure(figsize=(10, 6))
sns.histplot(distribution_pm25, kde=True, bins=30, color='green')
plt.title("Distribusi PM2.5")
plt.xlabel("PM2.5")
plt.ylabel("Frekuensi")
st.pyplot(plt.gcf())

# Visualisasi 4: Rata-rata PM2.5 berdasarkan Jam
st.subheader("Rata-rata PM2.5 Berdasarkan Jam")
plt.figure(figsize=(10, 6))
plt.plot(hourly_avg_pm25['hour'], hourly_avg_pm25['PM2.5'], marker='o', color='purple')
plt.title("Rata-rata PM2.5 Berdasarkan Jam")
plt.xlabel("Jam")
plt.ylabel("Rata-rata PM2.5")
st.pyplot(plt.gcf())

st.markdown("**Kesimpulan**")
st.markdown("1. Tren menunjukkan adanya fluktuasi rata-rata PM2.5 per bulan.")
st.markdown("2. Heatmap menunjukkan hubungan antara PM2.5 dengan faktor-faktor cuaca.")
st.markdown("3. Distribusi nilai PM2.5 memperlihatkan pola distribusi data dalam rentang tertentu.")
st.markdown("4. Analisis rata-rata PM2.5 per jam menunjukkan adanya perubahan polusi udara berdasarkan waktu dalam sehari.")
