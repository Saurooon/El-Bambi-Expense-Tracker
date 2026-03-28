import streamlit as st
import pandas as pd
from datetime import date
import os

# --- CONFIGURATION ---
DATA_FILE = "expenses.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# --- APP UI ---
st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("💸 Expense Tracker")

# Initialize data
df = load_data()

# Sidebar for Data Entry
with st.sidebar:
    st.header("Add New Expense")
    with st.form("expense_form", clear_on_submit=True):
        exp_date = st.date_input("Date", date.today())
        category = st.selectbox("Category", ["Food", "Transport", "Rent", "Utilities", "Entertainment", "Nicholas", "Coca-Cola", "Sysco", "Local Markets", "U.S. Foods", "Other"])
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        description = st.text_input("Description")
        
        submitted = st.form_submit_button("Add Expense")
        if submitted:
            new_data = pd.DataFrame([[exp_date, category, amount, description]], 
                                    columns=df.columns)
            df = pd.concat([df, new_data], ignore_index=True)
            save_data(df)
            st.success("Expense added!")

# --- DASHBOARD ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Recent Transactions")
    st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)

with col2:
    st.subheader("Spending by Category")
    if not df.empty:
        category_totals = df.groupby("Category")["Amount"].sum()
        st.pie_chart(category_totals)
    else:
        st.info("No data available yet.")

# Summary Metrics
st.divider()
total_spent = df["Amount"].sum()
st.metric("Total Spending to Date", f"${total_spent:,.2f}")
