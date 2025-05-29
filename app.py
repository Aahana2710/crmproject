import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="CRM Dashboard", layout="wide")

st.title("📊 CRM Dashboard")
st.write("This dashboard loads customer data directly from GitHub.")

# GitHub raw URL
github_url = "https://raw.githubusercontent.com/your-username/your-repo/main/customerdata100.xlsx"  # <-- Replace with your actual raw .xlsx URL

# Read Excel from GitHub
@st.cache_data
def load_data(url):
    return pd.read_excel(url)

df = load_data(github_url)

# Sidebar filters
st.sidebar.header("🔍 Filter Data")

city_filter = st.sidebar.multiselect("City", options=sorted(df['City'].dropna().unique()))
state_filter = st.sidebar.multiselect("State", options=sorted(df['State'].dropna().unique()))
country_filter = st.sidebar.multiselect("Country", options=sorted(df['Country'].dropna().unique()))
region_filter = st.sidebar.multiselect("Region", options=sorted(df['Region'].dropna().unique()))
product_filter = st.sidebar.multiselect("Product", options=sorted(df['Product'].dropna().unique()))

# Search by ID or Name
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
    filtered_df = filtered_df[filtered_df['Country'].isin(country_filter)]
if region_filter:
    filtered_df = filtered_df[filtered_df['Region'].isin(region_filter)]
if product_filter:
    filtered_df = filtered_df[filtered_df['Product'].isin(product_filter)]

if search_id:
    filtered_df = filtered_df[filtered_df['Customer ID'].str.contains(search_id, case=False, na=False)]
if search_name:
    filtered_df = filtered_df[filtered_df['Name'].str.contains(search_name, case=False, na=False)]

# Display
st.subheader("📄 Filtered Data")
st.dataframe(filtered_df, use_container_width=True)
st.success(f"Showing {len(filtered_df)} out of {len(df)} records.")
