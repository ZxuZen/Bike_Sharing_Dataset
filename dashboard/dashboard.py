import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

df_day = pd.read_csv('datasets/day.csv')
df_hour = pd.read_csv('datasets/hour.csv')

df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

st.title('Bike Sharing Dashboard')

data_option = st.sidebar.selectbox('Pilih Data', ['Daily', 'Hourly', 'RFM Analysis'])

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

    df_rfm = df_hour.copy()
    df_rfm['user_id'] = ...  

    current_date = df_rfm['dteday'].max()
    rfm_df = df_rfm.groupby('user_id').agg({
        'dteday': lambda x: (current_date - x.max()).days,  
        'cnt': ['count', 'sum'] 
    }).reset_index()
    
    rfm_df.columns = ['user_id', 'Recency', 'Frequency', 'Monetary']
    st.dataframe(rfm_df)

    fig, ax = plt.subplots()
    sns.histplot(rfm_df['Recency'], bins=30, ax=ax)
    plt.title('Distribution of Recency')
    st.pyplot(fig)

st.sidebar.markdown('**Informasi Tambahan**')
st.sidebar.markdown('- Dashboard ini menampilkan data peminjaman sepeda harian dan per jam.')
st.sidebar.markdown('- Anda dapat memilih data yang ingin ditampilkan di sidebar.')
