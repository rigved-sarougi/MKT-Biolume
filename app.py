import streamlit as st
import pandas as pd
import altair as alt

# Load the data from the CSV file in the repository
DATA_URL = "MKT+Biolume - Inventory System - Products McKingsTown - TP.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_URL)

# Load data
df = load_data()

# Dashboard Title
st.title("Product Performance Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
categories = st.sidebar.multiselect(
    "Select Product Categories", 
    options=df["Product Category"].unique(), 
    default=df["Product Category"].unique()
)
min_price, max_price = st.sidebar.slider(
    "Price Range", 
    min_value=int(df["Price"].min()), 
    max_value=int(df["Price"].max()), 
    value=(int(df["Price"].min()), int(df["Price"].max()))
)

# Filtered Data
filtered_df = df[
    (df["Product Category"].isin(categories)) & 
    (df["Price"].between(min_price, max_price))
]

# Key Metrics
total_products = filtered_df["Product ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()
avg_price = filtered_df["Price"].mean()

st.subheader("Key Metrics")
st.write(f"**Total Products:** {total_products}")
st.write(f"**Total Quantity Available:** {total_quantity}")
st.write(f"**Average Price:** ₹{avg_price:.2f}")

# Data Visualization
st.subheader("Product Category Distribution")
category_chart = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X("Product Category", sort="-y", title="Category"),
    y=alt.Y("Quantity", title="Quantity"),
    color="Product Category"
)
st.altair_chart(category_chart, use_container_width=True)

st.subheader("Product Price vs Quantity")
scatter_chart = alt.Chart(filtered_df).mark_circle(size=100).encode(
    x=alt.X("Price", title="Price (₹)"),
    y=alt.Y("Quantity", title="Quantity"),
    tooltip=["Product Name", "Price", "Quantity"],
    color="Product Category"
)
st.altair_chart(scatter_chart, use_container_width=True)

# Display Data Table
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Download Button
st.download_button(
    label="Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_products.csv",
    mime="text/csv"
)
