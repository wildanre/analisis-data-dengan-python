import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Baca dataset
data_path = "https://raw.githubusercontent.com/Danu313/analisis_data/main/main_data.csv"
df = pd.read_csv(data_path)

# Sidebar
with st.sidebar:
    
    st.header("Visualisasi Kualitas Udara")
   
    st.image("https://fin.co.id/upload/e2cd3031271e5036e3631e1c3a943588.jpeg")


    year_selection = st.selectbox("Pilih Tahun:", df['year'].unique())


    selected_dataset = st.radio("Pilih Set Data:", ['Dongsi', 'Aotizhongxin'])


selected_data = df[(df['year'] == year_selection) & (df['station'] == selected_dataset)]

#title
st.title(f'Analisis Kualitas Udara {selected_dataset} Tahun {year_selection}')

# Tampilkan data 
st.write(f"Data Tahun {year_selection} di stasiun {selected_dataset}:")
st.write(selected_data)

# Visualisasi rata-rata kualitas udara harian
st.subheader("Rata-rata Kualitas Udara Harian")
numeric_columns = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']

# Visualisasi menggunakan Seaborn
fig, ax = plt.subplots(figsize=(12, 8))
for column in numeric_columns:
    sns.lineplot(data=selected_data, x='day', y=column, label=column, ax=ax)

ax.set(xlabel='Hari', ylabel='Rata-rata Kualitas Udara',
       title=f'Rata-rata Kualitas Udara Harian Tahun {year_selection} - {selected_dataset}')
ax.legend()
st.pyplot(fig)

# Tampilkan kualitas udara pada hari tertentu jika tombol diklik
if st.button("Filter Kualitas Udara Untuk Hari Tertentu..."):
    selected_day = st.number_input("Masukkan tanggal (1-31):", min_value=1, max_value=31)
    day_data = selected_data[selected_data['day'] == selected_day]
    st.write(f"Kualitas Udara pada Hari ke-{selected_day}:", day_data[numeric_columns])

# Perbandingan antara suhu minimal dan maksimal, CO minimal dan maksimal
min_max_comparison = selected_data.agg({
    'TEMP': ['min', 'max'],
    'CO': ['min', 'max']
})

st.subheader("Perbandingan Suhu dan CO Minimal-Maksimal")

# Tabel untuk perbandingan suhu dan CO
st.write(min_max_comparison)

# Metrik: Rata-rata suhu setiap tahun
avg_temp_per_year = df.groupby('year')['TEMP'].mean()

# Tampilkan metrik suhu di sidebar
st.sidebar.metric(label="Rata-rata Suhu", value=f"{avg_temp_per_year[year_selection]:.2f} °C", delta="")

# Metrik: Perubahan suhu dari tahun sebelumnya
if year_selection > df['year'].min():
    delta_temp = avg_temp_per_year[year_selection] - avg_temp_per_year[year_selection - 1]
    st.sidebar.metric(label="Perubahan Temperatur", value=f"{delta_temp:.2f} °C", delta="")

# Visualisasi kualitas udara tahunan
st.subheader("V Rata-rata Kualitas Udara Tahunan")
avg_air_quality_per_year = df.groupby(['year', 'station'])[numeric_columns].mean().reset_index()

# Visualisasi menggunakan Seaborn
fig, ax = plt.subplots(figsize=(12, 8))
for column in numeric_columns:
    sns.lineplot(data=avg_air_quality_per_year, x='year', y=column, hue='station', marker='o', ax=ax)

ax.set(xlabel='Tahun', ylabel='Rata-rata Kualitas Udara',
       title=f'Rata-rata Kualitas Udara Tahunan - {selected_dataset}')
ax.legend(title='Station')
st.pyplot(fig)

# Perbandingan rata rata kualitas udara Dongsi_df dan Aotizhongxin_df
avg_air_quality_comparison = df.groupby(['station'])[numeric_columns].mean().reset_index()

# Line chart untuk perbandingan rata-rata kualitas udara antara Stasiun Dongsi dan Aotizhongxin
st.subheader("Perbandingan Rata-rata Kualitas Udara Antara Wilayah Dongsi dan Aotizhongxin")
fig, ax = plt.subplots(figsize=(12, 8))

for station in avg_air_quality_comparison['station']:
    station_data = avg_air_quality_per_year[avg_air_quality_per_year['station'] == station]
    sns.lineplot(data=station_data, x='year', y='PM2.5', label=f'{station} - PM2.5', marker='o', ax=ax)

ax.set(xlabel='Tahun', ylabel='Rata-rata Kualitas Udara (PM2.5)',
       title='Perbandingan Rata-rata Kualitas Udara Antara Dongsi dan Aotizhongxin')
ax.legend(title='Station')
st.pyplot(fig)

# Footer
st.caption('Copyright (c) Wildanu Dicoding 2023')

# Menangani peringatan
st.set_option('deprecation.showPyplotGlobalUse', False)
