# 🍔 Online Food Delivery Analysis: Data-Driven Business Insights

## Project Overview
This project analyzes 100,000 online food delivery orders to extract business insights using Python, SQL, and Power BI.

## Project Structure
```
online_food_delivery_analysis/
│
├── data/                        # Raw and cleaned datasets
│   ├── raw/                     # Original dataset
│   └── cleaned/                 # Preprocessed data
│
├── notebooks/                   # Jupyter Notebooks
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_feature_engineering.ipynb
│   └── 05_analytics.ipynb
│
├── scripts/                     # Python scripts
│   ├── data_cleaning.py
│   ├── eda.py
│   ├── feature_engineering.py
│   ├── analytics.py
│   └── db_upload.py
│
├── sql/                         # SQL scripts
│   ├── create_tables.sql
│   ├── insert_data.sql
│   └── analytical_queries.sql
│
├── dashboard/                   # Streamlit dashboard
│   └── app.py
│
├── outputs/                     # Charts and reports
│
├── docs/                        # Documentation
│
├── requirements.txt
└── README.md
```

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Place the dataset in `data/raw/`
3. Run notebooks in order (01 → 05) or execute scripts directly
4. For SQL: run `sql/create_tables.sql` then `scripts/db_upload.py`
5. For dashboard: `streamlit run dashboard/app.py`

## Dataset
[Download Dataset](https://drive.google.com/file/d/1ln_YbLXHZjah8c-zgrT_zacnfSwTB9ZE/view?usp=sharing)

## Skills Covered
- Python (Pandas, NumPy, Matplotlib, Seaborn)
- Data Cleaning & Preprocessing
- Exploratory Data Analysis (EDA)
- SQL & MySQL
- Power BI / Streamlit Dashboards
- KPI Design & Business Metrics
