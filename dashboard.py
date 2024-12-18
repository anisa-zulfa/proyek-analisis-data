import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from st_aggrid import AgGrid

# Set style untuk visualisasi
sns.set(style='darkgrid')

# Membaca data
data = pd.read_csv('main_data.csv')
data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'], errors='coerce')
data.dropna(subset=['order_purchase_timestamp', 'price'], inplace=True)

# Fungsi untuk menghitung total pengeluaran per kategori produk
def create_sum_order_items_df(data):
    sum_order_items_df = data.groupby('product_category_name')['price'].sum().reset_index()
    sum_order_items_df.columns = ['Product Category', 'Total Sales']
    return sum_order_items_df

# Fungsi untuk menghitung kategori produk dengan jumlah penjualan terbanyak dan tersedikit
def get_top_and_bottom_products(data):
    product_sales_df = data.groupby('product_category_name')['order_id'].count().reset_index()
    product_sales_df.columns = ['Product Category', 'Order Count']
    top_product = product_sales_df.loc[product_sales_df['Order Count'].idxmax()]
    bottom_product = product_sales_df.loc[product_sales_df['Order Count'].idxmin()]
    return top_product, bottom_product

# Fungsi untuk menghitung nilai rata-rata transaksi per order
def create_avg_order_value(data):
    avg_order_value_df = data.groupby('order_id')['price'].sum().reset_index()
    return avg_order_value_df['price'].mean()

# Fungsi untuk menghitung waktu transaksi terakhir
def get_last_transaction_date(data):
    return data['order_purchase_timestamp'].max()

# Fungsi untuk analisis RFM

def calculate_rfm(data):
    # Menghitung Recency, Frequency, dan Monetary
    recent_date = data['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
    rfm_df = data.groupby('customer_id').agg(
        recency=('order_purchase_timestamp', lambda x: (recent_date - x.max()).days),
        frequency=('order_id', 'nunique'),
        monetary=('price', 'sum')
    ).reset_index()

    # Memberikan ranking untuk Recency, Frequency, dan Monetary
    rfm_df['R_rank'] = rfm_df['recency'].rank(ascending=False)
    rfm_df['F_rank'] = rfm_df['frequency'].rank(ascending=False)
    rfm_df['M_rank'] = rfm_df['monetary'].rank(ascending=False)

    # Normalisasi rank pelanggan
    rfm_df['R_rank_norm'] = (rfm_df['R_rank'] / rfm_df['R_rank'].max()) * 100
    rfm_df['F_rank_norm'] = (rfm_df['F_rank'] / rfm_df['F_rank'].max()) * 100
    rfm_df['M_rank_norm'] = (rfm_df['M_rank'] / rfm_df['M_rank'].max()) * 100

    # Menghapus kolom ranking yang tidak dibutuhkan
    rfm_df.drop(columns=['R_rank', 'F_rank', 'M_rank'], inplace=True)

    # Menghitung skor RFM berdasarkan bobot
    rfm_df['RFM_Score'] = 0.15 * rfm_df['R_rank_norm'] + 0.28 * rfm_df['F_rank_norm'] + 0.57 * rfm_df['M_rank_norm']

    # Menyesuaikan skor dan membulatkan hasil
    rfm_df['RFM_Score'] = (rfm_df['RFM_Score'] * 0.05).round(2)

    # Menentukan segmentasi pelanggan berdasarkan RFM_Score
    rfm_df['Customer Segment'] = np.select(
        [
            (rfm_df['RFM_Score'] > 4.5),
            (rfm_df['RFM_Score'] > 4),
            (rfm_df['RFM_Score'] > 3),
            (rfm_df['RFM_Score'] > 1.6)
        ], 
        ['Top Customers', 'High Value Customers', 'Medium Value Customers', 'Low Value Customers'], 
        default='Lost Customers'
    )

    # Mengembalikan dataframe dengan hasil RFM
    return rfm_df[['customer_id', 'recency', 'frequency', 'monetary', 'RFM_Score', 'Customer Segment']]

# Streamlit Sidebar untuk Filter Waktu
st.sidebar.subheader('Filter Waktu')
start_date, end_date = st.sidebar.slider(
    'Pilih Rentang Waktu',
    min_value=data['order_purchase_timestamp'].min().date(),
    max_value=data['order_purchase_timestamp'].max().date(),
    value=(data['order_purchase_timestamp'].min().date(), data['order_purchase_timestamp'].max().date()),
    format="YYYY-MM-DD"
)

filtered_data = data[
    (data['order_purchase_timestamp'].dt.date >= start_date) & 
    (data['order_purchase_timestamp'].dt.date <= end_date)
]

# Streamlit Title
st.title('E-commerce Dashboard')

# fitur interaktif untuk mencari produk
search_term = st.text_input("Cari Produk", "")
filtered_search_data = filtered_data[filtered_data['product_category_name'].str.contains(search_term, case=False)]
AgGrid(filtered_search_data, editable=True, filter=True, sortable=True)

# Tabel Data Transaksi
st.subheader("Tabel Data Transaksi")
AgGrid(filtered_data, filter=True, sortable=True)

# Tampilkan Head dan Tail Data
st.subheader("Head dan Tail Data")
st.write("### Head Data")
st.write(filtered_data.head())

st.write("### Tail Data")
st.write(filtered_data.tail())

# Fitur Interaktif untuk Filter Berdasarkan Kategori Produk
st.sidebar.subheader('Filter Kategori Produk')
selected_category = st.sidebar.multiselect(
    'Pilih Kategori Produk:',
    options=data['product_category_name'].unique(),
    default=data['product_category_name'].unique().tolist()
)

filtered_category_data = filtered_data[filtered_data['product_category_name'].isin(selected_category)]

# Bar Chart 5 Kategori Produk Teratas
st.subheader('5 Kategori Produk Teratas Berdasarkan Jumlah Penjualan')
top_5_products = get_top_and_bottom_products(filtered_category_data)[0]
top_5_product_df = filtered_category_data.groupby('product_category_name')['order_id'].count().reset_index()
top_5_product_df = top_5_product_df.nlargest(5, 'order_id')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='order_id', y='product_category_name', data=top_5_product_df, color='skyblue', ax=ax)
ax.set_title('5 Kategori Produk Teratas')
ax.set_xlabel('Jumlah Penjualan')
ax.set_ylabel('Kategori Produk')
st.pyplot(fig)

# Bar Chart 5 Kategori Produk Terbawah
st.subheader('5 Kategori Produk Terbawah Berdasarkan Jumlah Penjualan')
bottom_5_products = get_top_and_bottom_products(filtered_category_data)[1]
bottom_5_product_df = filtered_category_data.groupby('product_category_name')['order_id'].count().reset_index()
bottom_5_product_df = bottom_5_product_df.nsmallest(5, 'order_id')
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x='order_id', y='product_category_name', data=bottom_5_product_df, color='salmon', ax=ax2)
ax2.set_title('5 Kategori Produk Terbawah')
ax2.set_xlabel('Jumlah Penjualan')
ax2.set_ylabel('Kategori Produk')
st.pyplot(fig2)

# Demografi Berdasarkan Kota
st.subheader('Tren Jumlah Pelanggan Berdasarkan Kota')
city_customer_count = filtered_category_data.groupby('customer_city')['customer_unique_id'].nunique().reset_index()
city_customer_count = city_customer_count.sort_values(by='customer_unique_id', ascending=False).head(10)
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(x='customer_unique_id', y='customer_city', data=city_customer_count, color='palegreen', ax=ax3)
ax3.set_title('Jumlah Pelanggan Berdasarkan Kota')
ax3.set_xlabel('Jumlah Pelanggan')
ax3.set_ylabel('Kota')
st.pyplot(fig3)

# Demografi Berdasarkan Provinsi
st.subheader('Tren Jumlah Pelanggan Berdasarkan Provinsi')
province_customer_count = filtered_category_data.groupby('customer_state')['customer_unique_id'].nunique().reset_index()
province_customer_count = province_customer_count.sort_values(by='customer_unique_id', ascending=False).head(10)
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.barplot(x='customer_unique_id', y='customer_state', data=province_customer_count, color='thistle', ax=ax4)
ax4.set_title('Jumlah Pelanggan Berdasarkan Provinsi')
ax4.set_xlabel('Jumlah Pelanggan')
ax4.set_ylabel('Provinsi')
st.pyplot(fig4)

# Tren Jumlah Pelanggan Berdasarkan Tahun Transaksi Terakhir
st.subheader('Tren Jumlah Pelanggan Berdasarkan Tahun Transaksi Terakhir')
filtered_category_data['transaction_year'] = filtered_category_data['order_purchase_timestamp'].dt.year
yearly_customer_count = filtered_category_data.groupby('transaction_year')['customer_unique_id'].nunique().reset_index()
fig5, ax5 = plt.subplots(figsize=(10, 6))
sns.lineplot(x='transaction_year', y='customer_unique_id', data=yearly_customer_count, marker='o', color='orange', ax=ax5)
ax5.set_title('Jumlah Pelanggan Berdasarkan Tahun Transaksi Terakhir')
ax5.set_xlabel('Tahun')
ax5.set_ylabel('Jumlah Pelanggan')
st.pyplot(fig5)

# Tampilkan Transaksi Terakhir
st.subheader('Transaksi Terakhir yang Paling Baru')
last_transaction = get_last_transaction_date(filtered_category_data)
st.write(f"**Transaksi terakhir tercatat pada:** {last_transaction.strftime('%Y-%m-%d')}")

# Distribusi Segmentasi Pelanggan (RFM)
st.subheader('Distribusi Segmentasi Pelanggan Berdasarkan RFM')
rfm_df = calculate_rfm(filtered_category_data)
fig6, ax6 = plt.subplots(figsize=(8, 8))
sizes = rfm_df['Customer Segment'].value_counts()
labels = sizes.index
ax6.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set3', len(sizes)))
ax6.set_title('Distribusi Segmentasi Pelanggan')
st.pyplot(fig6)

# Kesimpulan
st.header('Kesimpulan')
st.markdown("""
1.Produk yang Paling Banyak dan Paling Sedikit Terjual:
    Kategori "cama_mesa_banho", "moveis_decoracao", "beleza_saude", serta "informatica_acessorios" memiliki performa penjualan yang baik. Sementara itu, kategori "seguros_e_servicos","cds_dvds_musicais", dan "fashion_roupa_infanto_juvenil" cenderung kurang diminati oleh pelanggan.

2.Demografi Pelanggan:
    Pelanggan terbanyak berasal dari São Paulo dan Rio de Janeiro, baik di tingkat kota maupun provinsi, diikuti oleh Minas Gerais dan Rio Grande do Sul sebagai pasar potensial.

3.Kapan Terakhir Pelanggan Melakukan Transaksi:
    Transaksi terakhir tercatat pada 2018, menunjukkan adanya pelanggan yang tidak aktif dalam jangka waktu lama, sehingga diperlukan strategi untuk menarik mereka kembali.

4.Segmentasi Pelanggan
    Sebagian besar pelanggan termasuk dalam segmen Top Customers dan High Value Customers
""")