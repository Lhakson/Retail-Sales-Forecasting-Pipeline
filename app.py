import streamlit as st
import duckdb
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Retail Forecasting Dashboard", layout="wide")

@st.cache_data
def get_data():
    con = duckdb.connect('data/retail_warehouse.db')
    actuals = con.execute("SELECT * FROM processed_sales").df()
    forecast = con.execute("SELECT ds, yhat, yhat_lower, yhat_upper FROM sales_forecast").df()
    con.close()
    return actuals, forecast

st.title("📈 Retail Sales Forecasting Dashboard")
st.markdown("---")

try:
    df_actual, df_forecast = get_data()

    # Metrics
    col1, col2 = st.columns(2)
    latest_val = df_actual['value'].iloc[-1]
    latest_growth = df_actual['yoy_growth_pct'].iloc[-1]
    col1.metric("Latest Sales", f"${latest_val:,.0f}M")
    col2.metric("YoY Growth", f"{latest_growth:.1f}%")

    # Historical Chart
    fig1 = px.line(df_actual, x='date', y='value', title="Historical Sales Trend")
    st.plotly_chart(fig1, width='stretch')

    # Forecast Chart
    fig2 = px.line(df_forecast, x='ds', y='yhat', title="12-Month AI Forecast")
    st.plotly_chart(fig2, width='stretch')

except Exception as e:
    st.warning("Please run 'python main.py' first to generate the data.")