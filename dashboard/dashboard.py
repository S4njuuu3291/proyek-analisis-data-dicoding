import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import os

st.title("Analisis Data E-Commerce")

st.sidebar.title("Menu Analisis")
tabs = st.sidebar.radio("Pilih Analisis:", 
                        ["Analisis Kategori Produk", "Analisis Pengiriman", 
                         "Analisis Pembayaran", "Analisis Ulasan", 
                         "Analisis Produk", "Analisis Penjual", 
                         "Analisis Customer", "Analisis Order"])

def load_data():
    customers_df = pd.read_csv("data/customers_dataset.csv")
    geolocation_df = pd.read_csv("data/geolocation_dataset.csv")
    orders_df = pd.read_csv("data/orders_dataset.csv")
    order_items_df = pd.read_csv("data/order_items_dataset.csv")
    order_payments_df = pd.read_csv("data/order_payments_dataset.csv")
    order_reviews_df = pd.read_csv("data/order_reviews_dataset.csv")
    product_category_name_tr_df = pd.read_csv("data/product_category_name_translation.csv")
    products_df = pd.read_csv("data/products_dataset.csv")
    sellers_df = pd.read_csv("data/sellers_dataset.csv")
    orders_all = pd.read_csv("data/orders_all.csv")
    return customers_df, geolocation_df, orders_df, order_items_df, order_payments_df, order_reviews_df, product_category_name_tr_df, products_df, sellers_df, orders_all

customers_df, geolocation_df, orders_df, order_items_df, order_payments_df, order_reviews_df, product_category_name_tr_df, products_df, sellers_df, orders_all = load_data()

def plot_bar_chart(data, x_column, y_column, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x=data[x_column], height=data[y_column])
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    st.pyplot(fig)

def display_metrics(data, label_column, value_column, index):
    col1, col2 = st.columns(2)
    col1.metric(label_column, data[label_column].iloc[index])
    col2.metric(value_column, data[value_column].iloc[index])

if tabs == "Analisis Kategori Produk":
    st.header("Kategori Produk dengan Pembelian Terbanyak")
    
    product_purchase_counts = pd.read_csv("data/product_purchase_counts.csv")
    product_purchase_counts.sort_values(by='count', ascending=False, inplace=True)
    product_purchase_counts = product_purchase_counts.head(10)
    
    plot_bar_chart(product_purchase_counts, "product_category_name", "count", 
                   "Kategori Produk dengan Pembelian Terbanyak", "Kategori Produk", "Jumlah Pembelian")
    
    display_metrics(product_purchase_counts, "product_category_name", "count", 0)

elif tabs == "Analisis Pengiriman":
    st.header("Pengaruh Kecepatan Pengiriman terhadap Skor Ulasan")
    
    average_review_scores = pd.read_csv("data/average_review_scores.csv")
    
    plot_bar_chart(average_review_scores, "Ontime", "review_score", 
                   "Pengaruh Kecepatan Pengiriman terhadap Skor Ulasan", "Kecepatan Pengiriman", "Skor Ulasan")
    
    display_metrics(average_review_scores, "Ontime", "review_score", 1)

elif tabs == "Analisis Pembayaran":
    st.header("Jumlah Pembayaran Berdasarkan Metode")
    
    payment_type = orders_all['payment_type'].value_counts()
    st.write(payment_type)

elif tabs == "Analisis Ulasan":
    st.header("Jumlah Ulasan Berdasarkan Skor")
    
    review_score = order_reviews_df.groupby(by='review_score').order_id.nunique().sort_values(ascending=True)
    st.write(review_score)

elif tabs == "Analisis Produk":
    st.header("Informasi Produk Berdasarkan Kategori")
    
    product_category = products_df.groupby(by='product_category_name').agg({
        "product_id": "nunique",
        "product_weight_g": ["max", "min", "mean"],
        "product_length_cm": ["max", "min", "mean"],
        "product_height_cm": ["max", "min", "mean"],
        "product_width_cm": ["max", "min", "mean"],
    })
    
    st.write(product_category)

elif tabs == "Analisis Penjual":
    st.header("Jumlah Penjual Berdasarkan Kota dan Negara Bagian")
    
    seller_city = sellers_df.groupby(by='seller_city').seller_id.nunique().sort_values(ascending=False)
    seller_state = sellers_df.groupby(by='seller_state').seller_id.nunique().sort_values(ascending=False)
    
    st.write("Jumlah penjual berdasarkan kota:")
    st.write(seller_city)
    st.write("Jumlah penjual berdasarkan negara bagian:")
    st.write(seller_state)

elif tabs == "Analisis Customer":
    st.header("Analisis Customer Berdasarkan Kota dan Negara Bagian")
    
    customer_city = customers_df.groupby(by='customer_city').customer_id.nunique().sort_values(ascending=False)
    customer_state = customers_df.groupby(by='customer_state').customer_id.nunique().sort_values(ascending=False)
    
    st.write("Jumlah customer berdasarkan kota:")
    st.write(customer_city)
    st.write("Jumlah customer berdasarkan negara bagian:")
    st.write(customer_state)

elif tabs == "Analisis Order":
    st.header("Analisis Order Berdasarkan Status dan Pengiriman")
    
        # Ensure that the columns are datetime
    orders_df['order_delivered_customer_date'] = pd.to_datetime(orders_df['order_delivered_customer_date'])
    orders_df['order_delivered_carrier_date'] = pd.to_datetime(orders_df['order_delivered_carrier_date'])
    orders_df['order_estimated_delivery_date'] = pd.to_datetime(orders_df['order_estimated_delivery_date'])

    # Calculate delivery time and estimated delivery time
    delivery_time = (orders_df['order_delivered_customer_date'] - orders_df['order_delivered_carrier_date']).dt.total_seconds() / 86400
    orders_df['delivery_time'] = round(delivery_time)

    estimated_delivery_time = (orders_df['order_estimated_delivery_date'] - orders_df['order_delivered_carrier_date']).dt.total_seconds() / 86400
    orders_df['estimated_delivery_time'] = round(estimated_delivery_time)

    
    order_status = orders_df['order_status'].value_counts()
    st.write("Jumlah order berdasarkan status:")
    st.write(order_status)
    st.write("Persentase pesanan sampai sesuai/lebih cepat dari estimasi pengiriman:")
    st.write((orders_df['delivery_time'] > orders_df['estimated_delivery_time']).value_counts())

