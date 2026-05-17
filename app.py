import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="PhonePe Insights", layout="wide")

# Title
st.title("📊 PhonePe Transaction Insights Dashboard")

# Load data
df = pd.read_csv("cleaned_phonepe_transactions.csv")

# =========================
# 🔹 SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Filters")

selected_state = st.sidebar.multiselect(
    "Select State",
    options=df['state'].unique(),
    default=df['state'].unique()
)

selected_year = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df['year'].unique()),
    default=sorted(df['year'].unique())
)

selected_type = st.sidebar.multiselect(
    "Transaction Type",
    options=df['transaction_type'].unique(),
    default=df['transaction_type'].unique()
)

# Apply filters
filtered_df = df[
    (df['state'].isin(selected_state)) &
    (df['year'].isin(selected_year)) &
    (df['transaction_type'].isin(selected_type))
]

# =========================
# 🔹 KPI METRICS
# =========================
total_amount = filtered_df['amount'].sum()
total_count = filtered_df['count'].sum()

col1, col2 = st.columns(2)

col1.metric("💰 Total Transaction Amount", f"{total_amount:,.0f}")
col2.metric("🔢 Total Transactions", f"{total_count:,.0f}")

# =========================
# 🔹 TOP STATES CHART
# =========================
st.subheader("🏆 Top 10 States by Transaction Amount")

top_states = (
    filtered_df.groupby("state")["amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_states)

# =========================
# 🔹 TRANSACTION TYPE CHART
# =========================
st.subheader("💳 Transaction Type Distribution")

txn_type = (
    filtered_df.groupby("transaction_type")["amount"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(txn_type)

# =========================
# 🔹 YEARLY TREND
# =========================
st.subheader("📈 Year-wise Growth")

year_trend = filtered_df.groupby("year")["amount"].sum()

st.line_chart(year_trend)

# =========================
# 🔹 RAW DATA VIEW (OPTIONAL)
# =========================
if st.checkbox("Show Raw Data"):
    st.write(filtered_df)
