import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="CRM Dashboard (India)",layout="wide")
st.title(" CRM Dashboard")

# Load the Excel file
@st.cache_data
def load_data():
    return pd.read_excel("indian_customerdata100.xlsx")

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Customers")

city_filter = st.sidebar.multiselect("City", sorted(df['City'].unique()))
state_filter = st.sidebar.multiselect("State", sorted(df['State'].unique()))
country_filter = st.sidebar.selectbox("Country", sorted(df['Country'].unique()))

region_filter = st.sidebar.multiselect("Region", sorted(df['Region'].unique()))
product_filter = st.sidebar.multiselect("Product", sorted(df['Product'].unique()))

# Text search
st.sidebar.subheader("🔎 Search")
search_id = st.sidebar.text_input("Customer ID")
search_name = st.sidebar.text_input("Customer Name")

# Apply filters
filtered_df = df.copy()

if city_filter:
    filtered_df = filtered_df[filtered_df['City'].isin(city_filter)]
if state_filter:
    filtered_df = filtered_df[filtered_df['State'].isin(state_filter)]
if country_filter:
    filtered_df = df[df['Country'] == country_filter]
if region_filter:
    filtered_df = filtered_df[filtered_df['Region'].isin(region_filter)]
if product_filter:
    filtered_df = filtered_df[filtered_df['Product'].isin(product_filter)]

if search_id:
    filtered_df = filtered_df[filtered_df['Customer ID'].str.contains(search_id, case=False)]
if search_name:
    filtered_df = filtered_df[filtered_df['Name'].str.contains(search_name, case=False)]

# Display data
st.subheader("📄 Filtered Data")
st.dataframe(filtered_df, use_container_width=True)
st.success(f"Showing {len(filtered_df)} out of {len(df)} records.")
