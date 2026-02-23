import streamlit as st
import duckdb
import plotly.express as px
import pandas as pd
import os

st.set_page_config(page_title="Retail Forecast", layout="wide")

# This helps us see if the file actually exists on the server
db_exists = os.path.exists('data/retail_warehouse.db')

st.title("📈 Retail Sales Intelligence Dashboard")

if not db_exists:
    st.error("⚠️ Database file not found in 'data/' folder. Please check your GitHub upload.")
else:
    try:
        # Connect directly without using the src modules for now
        con = duckdb.connect('data/retail_warehouse.db')
        
        # Pull the data
        df_act = con.execute("SELECT * FROM processed_sales").df()
        df_fcast = con.execute("SELECT ds, yhat FROM sales_forecast").df()
        con.close()

        # Display Metrics
        col1, col2 = st.columns(2)
        latest_val = df_act['value'].iloc[-1]
        col1.metric("Latest Sales", f"${latest_val:,.0f}M")
        col2.metric("Status", "Data Loaded Successfully")

        # Charts
        st.subheader("Historical Sales Trend")
        st.plotly_chart(px.line(df_act, x='date', y='value'), use_container_width=True)

        st.subheader("12-Month AI Forecast")
        st.plotly_chart(px.line(df_fcast, x='ds', y='yhat'), use_container_width=True)

    except Exception as e:
        st.error(f"Error reading database: {e}")