import streamlit as st
import pandas as pd

# Simple username-password dictionary
users = {
    "admin": "admin123",
    "aahana": "crmrocks",
    "testuser": "test123"
}

# Page setup
st.set_page_config(page_title="CRM Dashboard (India)", layout="wide")

# --- Login Check ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.sidebar.title("🔐 Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.success(f"Welcome, {username}!")
        else:
            st.error("❌ Invalid username or password")
    st.stop()

# Load the Excel file
@st.cache_data
def load_data():
    return pd.read_excel("indian_customerdata100_final.xlsx")

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Customers")

city_filter = st.sidebar.multiselect("City", sorted(df['City'].dropna().unique()))
state_filter = st.sidebar.multiselect("State", sorted(df['State'].dropna().unique()))
country_filter = st.sidebar.selectbox("Country", sorted(df['Country'].dropna().unique()))
region_filter = st.sidebar.multiselect("Region", sorted(df['Region'].dropna().unique()))
product_filter = st.sidebar.multiselect("Product", sorted(df['Product'].dropna().unique()))
company_filter = st.sidebar.multiselect("Company", sorted(df['Company'].dropna().unique()))

# Age range filter
age_category = st.sidebar.selectbox("Age Group", ["All", "0–10", "11–20", "21–30", "31–40", "41+"])

# 📊 Price category filter
price_category = st.sidebar.selectbox(
    "Price Category",
    ["All", "Less than ₹5,000", "₹5,000–₹10,000", "₹10,001–₹20,000", "₹20,001–₹50,000", "Above ₹50,000"]
)

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
    filtered_df = filtered_df[filtered_df['Country'] == country_filter]
if region_filter:
    filtered_df = filtered_df[filtered_df['Region'].isin(region_filter)]
if product_filter:
    filtered_df = filtered_df[filtered_df['Product'].isin(product_filter)]
if company_filter:
    filtered_df = filtered_df[filtered_df['Company'].isin(company_filter)]

# Age category filtering
if age_category != "All":
    if age_category == "0–10":
        filtered_df = filtered_df[filtered_df['Age'] <= 10]
    elif age_category == "11–20":
        filtered_df = filtered_df[(filtered_df['Age'] >= 11) & (filtered_df['Age'] <= 20)]
    elif age_category == "21–30":
        filtered_df = filtered_df[(filtered_df['Age'] >= 21) & (filtered_df['Age'] <= 30)]
    elif age_category == "31–40":
        filtered_df = filtered_df[(filtered_df['Age'] >= 31) & (filtered_df['Age'] <= 40)]
    elif age_category == "41+":
        filtered_df = filtered_df[filtered_df['Age'] >= 41]

# Price category filtering
if price_category != "All":
    if price_category == "Less than ₹5,000":
        filtered_df = filtered_df[filtered_df['Price'] < 5000]
    elif price_category == "₹5,000–₹10,000":
        filtered_df = filtered_df[(filtered_df['Price'] >= 5000) & (filtered_df['Price'] <= 10000)]
    elif price_category == "₹10,001–₹20,000":
        filtered_df = filtered_df[(filtered_df['Price'] > 10000) & (filtered_df['Price'] <= 20000)]
    elif price_category == "₹20,001–₹50,000":
        filtered_df = filtered_df[(filtered_df['Price'] > 20000) & (filtered_df['Price'] <= 50000)]
    elif price_category == "Above ₹50,000":
        filtered_df = filtered_df[filtered_df['Price'] > 50000]

# Search filters
if search_id:
    filtered_df = filtered_df[filtered_df['Customer ID'].astype(str).str.contains(search_id, case=False)]
if search_name:
    filtered_df = filtered_df[filtered_df['Name'].str.contains(search_name, case=False)]

# Display applied filters
st.subheader("🧾 Applied Filters")

if state_filter:
    st.write("State:", ", ".join(state_filter))
if city_filter:
    st.write("City:", ", ".join(city_filter))
if country_filter:
    st.write("Country:", country_filter)
if region_filter:
    st.write("Region:", ", ".join(region_filter))
if product_filter:
    st.write("Product:", ", ".join(product_filter))
if company_filter:
    st.write("Company:", ", ".join(company_filter))
if age_category != "All":
    st.write("Age Group:", age_category)
if price_category != "All":
    st.write("Price Category:", price_category)
if search_id:
    st.write("Customer ID contains:", search_id)
if search_name:
    st.write("Customer Name contains:", search_name)
import plotly.express as px

# --- Visualization Section ---
st.subheader("📈 Visualizations")

# 1. Top Selling Products - Bar Chart
product_counts = filtered_df['Product'].value_counts().reset_index()
product_counts.columns = ['Product', 'Count']

if not product_counts.empty:
    st.markdown("### 🛍️ Top Selling Products")
    fig_product = px.bar(product_counts, x='Product', y='Count', color='Product',
                         title="Most Sold Products", text='Count')
    st.plotly_chart(fig_product, use_container_width=True)
else:
    st.info("No product data to display for the selected filters.")

# 2. Age Distribution - Pie Chart
age_distribution = filtered_df['Age'].dropna()

if not age_distribution.empty:
    # Group into buckets
    age_bins = [0, 10, 20, 30, 40, 100]
    age_labels = ['0–10', '11–20', '21–30', '31–40', '41+']
    age_groups = pd.cut(age_distribution, bins=age_bins, labels=age_labels, right=True)

    age_group_counts = age_groups.value_counts().reset_index()
    age_group_counts.columns = ['Age Group', 'Count']

    st.markdown("### 👶🧓 Customer Age Distribution")
    fig_age = px.pie(age_group_counts, names='Age Group', values='Count', 
                     title="Customer Age Distribution", hole=0.3)
    st.plotly_chart(fig_age, use_container_width=True)
else:
    st.info("No age data to display for the selected filters.")


# Display filtered data
st.subheader("📄 Filtered Data")
st.dataframe(filtered_df, use_container_width=True)
st.success(f"Showing {len(filtered_df)} out of {len(df)} records.")




