# 📈 Retail Sales Intelligence & AI Forecasting Pipeline

An end-to-end data engineering pipeline that automates the extraction, transformation, and forecasting of retail sales data using Python, DuckDB, and Facebook Prophet.

![Dashboard Preview](https://via.placeholder.com/800x400?text=Insert+Your+Dashboard+Screenshot+Here)

## 🚀 Overview
This project addresses the "Data Graveyard" and "Stale Forecast" problems in retail. It automates the flow of data from raw API ingestion to a live executive dashboard, providing 12-month predictive insights with holiday-adjustment logic.

## 🛠️ Tech Stack
* **Language:** Python 3.13
* **Database:** DuckDB (OLAP-optimized local data warehouse)
* **AI/ML:** Facebook Prophet (Time-series forecasting)
* **Visualization:** Streamlit & Plotly
* **Orchestration:** Modular Python ETL pattern

## 🏗️ Architecture
The pipeline follows a clean "Modular ETL" architecture:
1.  **Ingestion Layer:** Connects to Alpha Vantage API with built-in request timeouts and error handling.
2.  **Storage Layer:** Uses DuckDB with **Primary Key constraints** to ensure data idempotency (no duplicate records).
3.  **Transformation Layer:** Utilizes **SQL Window Functions** (LAG) to calculate Year-over-Year (YoY) growth and growth deltas.
4.  **Forecasting Layer:** Implements a Prophet model configured with **US Holiday effects** to account for retail seasonality.



## 📊 Key Features
* **Idempotent Loading:** The pipeline can be run multiple times daily without duplicating data or breaking the schema.
* **Holiday-Aware AI:** The model automatically adjusts for Black Friday, Christmas, and other major US retail drivers.
* **Defensive Programming:** Includes logging, environment variable protection (.env), and division-by-zero SQL protection.

## ⚙️ Setup & Installation
1. Clone the repo: `git clone https://github.com/Lhakson/your-repo-name.git`
2. Create venv: `python -m venv venv`
3. Activate venv: `.\venv\Scripts\Activate.ps1`
4. Install dependencies: `pip install -r requirements.txt`
5. Add your API Key to a `.env` file: `ALPHA_VANTAGE_KEY=your_key`
6. Run the pipeline: `python main.py`
7. Launch Dashboard: `streamlit run app.py`

## 📈 Future Roadmap
* Add MAPE (Mean Absolute Percentage Error) tracking to monitor model drift.
* Containerize the application using Docker for cloud deployment.
* Integrate multi-series forecasting for specific retail categories.
