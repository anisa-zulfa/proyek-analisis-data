import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Membaca data
main_data = pd.read_csv('main_data.csv')

# Fungsi untuk menghitung total transaksi harian
def create_daily_orders_df(data):
    data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])
    daily_orders_df = data.groupby(data['order_purchase_timestamp'].dt.date)['order_id'].nunique().reset_index()
    daily_orders_df.columns = ['Date', 'Total Orders']
    return daily_orders_df

# Fungsi untuk menghitung total pengeluaran per produk
def create_sum_order_items_df(data):
    sum_order_items_df = data.groupby('product_id')['price'].sum().reset_index()
    sum_order_items_df.columns = ['Product ID', 'Total Sales']
    return sum_order_items_df

# Fungsi untuk menghitung transaksi per status order
def create_order_status_df(data):
    order_status_df = data.groupby('order_status').size().reset_index(name='Order Count')
    return order_status_df

# Fungsi untuk menghitung total penjualan berdasarkan kategori produk
def create_product_category_sales_df(data):
    product_category_sales_df = data.groupby('product_category_name')['price'].sum().reset_index()
    product_category_sales_df.columns = ['Product Category', 'Total Sales']
    return product_category_sales_df

# Fungsi untuk menghitung total penjualan harian
def create_daily_sales_df(data):
    data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])
    daily_sales_df = data.groupby(data['order_purchase_timestamp'].dt.date)['price'].sum().reset_index()
    daily_sales_df.columns = ['Date', 'Total Sales']
    return daily_sales_df

# Fungsi untuk menghitung nilai rata-rata transaksi per order
def create_avg_order_value_df(data):
    avg_order_value_df = data.groupby('order_id')['price'].sum().reset_index()
    avg_order_value = avg_order_value_df['price'].mean()
    return avg_order_value

# Menggunakan Streamlit untuk visualisasi
st.title('E-commerce Dashboard')

# Total Orders & Total Revenue Metrics
daily_orders_df = create_daily_orders_df(main_data)
daily_sales_df = create_daily_sales_df(main_data)

col1, col2 = st.columns(2)
with col1:
    total_orders = daily_orders_df['Total Orders'].sum()
    st.metric("Total Orders", total_orders)

with col2:
    total_revenue = format_currency(daily_sales_df['Total Sales'].sum(), "USD", locale='en_US')
    st.metric("Total Revenue", total_revenue)

# Grafik Jumlah Order Harian
st.subheader('Daily Orders')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(daily_orders_df['Date'], daily_orders_df['Total Orders'], marker='o', color='blue', linewidth=2)
ax.set_title('Orders Per Day', fontsize=16)
ax.set_xlabel('Date')
ax.set_ylabel('Order Count')
st.pyplot(fig)

# Grafik Penjualan Per Kategori Produk
st.subheader('Sales by Product Category')
product_category_sales_df = create_product_category_sales_df(main_data)
fig2, ax2 = plt.subplots(figsize=(16, 8))
sns.barplot(x='Product Category', y='Total Sales', data=product_category_sales_df, ax=ax2)
ax2.set_title('Sales by Product Category', fontsize=16)
ax2.set_xlabel('Product Category')
ax2.set_ylabel('Total Sales')
st.pyplot(fig2)

# Rata-rata Nilai Transaksi
st.subheader('Average Order Value')
avg_order_value = create_avg_order_value_df(main_data)
st.metric("Average Order Value", format_currency(avg_order_value, "USD", locale='en_US'))
