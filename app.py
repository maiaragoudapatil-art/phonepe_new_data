import streamlit as st
import pandas as pd

# =========================
# 🔹 PAGE CONFIG
# =========================
st.set_page_config(page_title="PhonePe Insights", layout="wide")

# =========================
# 🔹 LOAD DATA
# =========================
df = pd.read_csv("cleaned_phonepe_transactions.csv")

# =========================
# 🔹 TITLE
# =========================
st.title("📊 PhonePe Transaction Insights")

# =========================
# 🔹 SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Filters")

# Multi-select state
states = st.sidebar.multiselect(
    "Select State",
    options=sorted(df['state'].unique()),
    default=sorted(df['state'].unique())
)

# Year filter (optional but useful)
years = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df['year'].unique()),
    default=sorted(df['year'].unique())
)

# Apply filters
filtered_df = df[
    (df['state'].isin(states)) &
    (df['year'].isin(years))
]

# Safety check
if filtered_df.empty:
    st.warning("No data available for selected filters")
    st.stop()

# =========================
# 🔹 KPI SECTION
# =========================
st.subheader("Overview")

col1, col2 = st.columns(2)

total_amount = filtered_df['amount'].sum()
total_count = filtered_df['count'].sum()

col1.metric("💰 Total Amount", f"{total_amount:,.0f}")
col2.metric("🔢 Total Transactions", f"{total_count:,.0f}")

# =========================
# 🔹 TABS
# =========================
tab1, tab2, tab3 = st.tabs(["🏆 Top States", "💳 Categories", "📈 Trends"])

# -------------------------
# 🔹 TAB 1: TOP STATES
# -------------------------
with tab1:
    st.subheader("Top 10 States by Transaction Amount")

    top_states = (
        filtered_df.groupby("state")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(top_states)

# -------------------------
# 🔹 TAB 2: CATEGORIES
# -------------------------
with tab2:
    st.subheader("Transaction Type Distribution")

    txn_type = (
        filtered_df.groupby("transaction_type")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(txn_type)

# -------------------------
# 🔹 TAB 3: TRENDS
# -------------------------
with tab3:
    st.subheader("Year-wise Growth")

    trend = (
        filtered_df.groupby("year")["amount"]
        .sum()
    )

    st.line_chart(trend)

# =========================
# 🔹 RAW DATA (OPTIONAL)
# =========================
with st.expander("🔍 Show Raw Data"):
    st.dataframe(filtered_df)
