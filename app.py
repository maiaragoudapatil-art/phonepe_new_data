import streamlit as st
import pandas as pd

st.title("PhonePe Transaction Insights")
# load your CSV
df = pd.read_csv("cleaned_phonepe_transactions.csv")

st.subheader("Top 10 States by Transaction Amount")

top_states = df.groupby("state")["amount"].sum().sort_values(ascending=False).head(10)

st.bar_chart(top_states)
