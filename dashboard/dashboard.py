import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import folium
import geopandas as gpd
import streamlit.components.v1 as components


# Load datasets
df_day = pd.read_csv('datasets/day.csv')
df_hour = pd.read_csv('datasets/hour.csv')

# Convert date columns
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# Streamlit dashboard title
st.title('Bike Sharing Dashboard')

# Sidebar data option selection
data_option = st.sidebar.selectbox('Pilih Data', ['Daily', 'Hourly', 'RFM Analysis', 'Geospatial Analysis'])

if data_option == 'Daily':
    st.header('Daily Bike Sharing Data')

    season_avg = df_day.groupby('season')['cnt'].mean().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=season_avg, x='season', y='cnt', ax=ax)
    plt.title('Rata-rata Peminjaman Sepeda Berdasarkan Musim')
    plt.xlabel('Musim')
    plt.ylabel('Rata-rata Peminjaman')
    plt.xticks(ticks=range(4), labels=['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur'])
    st.pyplot(fig)

    corr = df_day.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    plt.title('Korelasi Antar Variabel')
    st.pyplot(fig)

elif data_option == 'Hourly':
    st.header('Hourly Bike Sharing Data')

    fig, ax = plt.subplots()
    sns.lineplot(data=df_hour, x='hr', y='cnt', estimator='mean', ax=ax)
    plt.title('Tren Penggunaan Sepeda Sepanjang Hari')
    plt.xlabel('Jam')
    plt.ylabel('Rata-rata Peminjaman')
    plt.xticks(range(0, 24))
    st.pyplot(fig)

    grouped = df_hour.groupby(['weekday', 'workingday'])['cnt'].sum().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=grouped, x='weekday', y='cnt', hue='workingday', ax=ax)
    plt.title('Penggunaan Sepeda Berdasarkan Hari dan Status Kerja')
    plt.xlabel('Hari')
    plt.ylabel('Jumlah Peminjaman')
    st.pyplot(fig)

elif data_option == 'RFM Analysis':
    st.header('RFM Analysis')

    # Assuming you have a user ID column and the cnt represents rentals
    df_rfm = df_hour.copy()
    df_rfm['user_id'] = ...  # Add your user ID logic here

    # Calculate Recency, Frequency, and Monetary
    current_date = df_rfm['dteday'].max()
    rfm_df = df_rfm.groupby('user_id').agg({
        'dteday': lambda x: (current_date - x.max()).days,  # Recency
        'cnt': ['count', 'sum']  # Frequency and Monetary
    }).reset_index()
    
    rfm_df.columns = ['user_id', 'Recency', 'Frequency', 'Monetary']
    st.dataframe(rfm_df)

    # Display RFM distribution
    fig, ax = plt.subplots()
    sns.histplot(rfm_df['Recency'], bins=30, ax=ax)
    plt.title('Distribution of Recency')
    st.pyplot(fig)

elif data_option == 'Geospatial Analysis':
    st.header('Geospatial Analysis')

    # Cek kolom yang ada
    st.write("Kolom yang ada di df_hour:", df_hour.columns)

    # Pastikan kolom lat dan lon ada
    if 'lat' in df_hour.columns and 'lon' in df_hour.columns:
        # Membuat GeoDataFrame
        geometry = gpd.points_from_xy(df_hour.lon, df_hour.lat)
        geo_df = gpd.GeoDataFrame(df_hour, geometry=geometry)

        # Membuat peta
        m = folium.Map(location=[geo_df.lat.mean(), geo_df.lon.mean()], zoom_start=12)

        for idx, row in geo_df.iterrows():
            folium.CircleMarker(
                location=(row['lat'], row['lon']),
                radius=row['cnt'] / 100,
                color='blue',
                fill=True,
                fill_color='blue',
                fill_opacity=0.6,
                popup=f"Peminjaman: {row['cnt']}"
            ).add_to(m)

        # Simpan peta ke file HTML
        m.save('bike_sharing_map.html')

        # Membaca file HTML dan menampilkannya di Streamlit
        HtmlFile = open('bike_sharing_map.html', 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        components.html(source_code, height=600)
    else:
        st.error("Kolom 'lat' dan 'lon' tidak ditemukan dalam dataset.")

st.sidebar.markdown('**Informasi Tambahan**')
st.sidebar.markdown('- Dashboard ini menampilkan data peminjaman sepeda harian dan per jam.')
st.sidebar.markdown('- Anda dapat memilih data yang ingin ditampilkan di sidebar.')
