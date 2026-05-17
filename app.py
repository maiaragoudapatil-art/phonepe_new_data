import streamlit as st
import pandas as pd

st.set_page_config(page_title="PhonePe Insights", layout="wide")

# Title
st.title("📊 PhonePe Transaction Insights")

# Load data
df = pd.read_csv("cleaned_phonepe_transactions.csv")

# =========================
# 🔹 SIDEBAR FILTER
# =========================
st.sidebar.header("Filters")

state = st.sidebar.selectbox(
    "Select State",
    ["All"] + list(df['state'].unique())
)

if state != "All":
    df = df[df['state'] == state]

# =========================
# 🔹 KPI SECTION
# =========================
st.subheader("Overview")

col1, col2 = st.columns(2)

col1.metric("💰 Total Amount", f"{df['amount'].sum():,.0f}")
col2.metric("🔢 Total Transactions", f"{df['count'].sum():,.0f}")

# =========================
# 🔹 TABS (KEY IMPROVEMENT)
# =========================
tab1, tab2, tab3 = st.tabs(["🏆 Top States", "💳 Categories", "📈 Trends"])

# -------------------------
# TAB 1: Top States
# -------------------------
with tab1:
    st.subheader("Top 10 States")

    top_states = (
        df.groupby("state")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(top_states)

# -------------------------
# TAB 2: Categories
# -------------------------
with tab2:
    st.subheader("Transaction Types")

    txn_type = df.groupby("transaction_type")["amount"].sum()

    st.bar_chart(txn_type)

# -------------------------
# TAB 3: Trends
# -------------------------
with tab3:
    st.subheader("Year-wise Growth")

    trend = df.groupby("year")["amount"].sum()

    st.line_chart(trend)

# =========================
# 🔹 RAW DATA (OPTIONAL)
# =========================
with st.expander("Show Raw Data"):
    st.dataframe(df)
