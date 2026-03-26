"""
Step 6: Upload Cleaned Data to MySQL
Online Food Delivery Analysis Project
"""

import pandas as pd
from sqlalchemy import create_engine, text
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# CONFIGURATION — Update with your credentials
# ─────────────────────────────────────────────
DB_CONFIG = {
    'host'    : 'localhost',
    'port'    : 3306,
    'user'    : 'root',
    'password': 'your_password',   # ← Change this
    'database': 'food_delivery_db'
}

DATA_PATH = "data/cleaned/featured_food_delivery.csv"


def get_engine():
    url = (f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
           f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    engine = create_engine(url, echo=False)
    return engine


def create_database(engine):
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}"))
    print(f"✅ Database '{DB_CONFIG['database']}' ready")


def upload_table(df: pd.DataFrame, table_name: str, engine, if_exists='replace'):
    """Upload a DataFrame to MySQL table."""
    df.to_sql(table_name, con=engine, if_exists=if_exists, index=False,
              chunksize=5000, method='multi')
    count = pd.read_sql(f"SELECT COUNT(*) AS cnt FROM {table_name}", engine).iloc[0, 0]
    print(f"  ✅ {table_name}: {count:,} rows uploaded")


def run_upload():
    print("\n📤 UPLOADING DATA TO MYSQL\n" + "=" * 40)

    df = pd.read_csv(DATA_PATH)
    print(f"Dataset loaded: {df.shape[0]:,} rows, {df.shape[1]} columns")

    engine = get_engine()

    # ── Upload main table ──
    upload_table(df, 'food_orders', engine)

    # ── Upload dimension slices ──
    # Customer dimension
    customer_cols = [c for c in df.columns if 'customer' in c.lower()]
    if customer_cols:
        customers_df = df[customer_cols].drop_duplicates()
        upload_table(customers_df, 'dim_customers', engine)

    # Restaurant dimension
    restaurant_cols = [c for c in df.columns if 'restaurant' in c.lower()]
    if restaurant_cols:
        restaurant_df = df[restaurant_cols].drop_duplicates()
        upload_table(restaurant_df, 'dim_restaurants', engine)

    print("\n🎉 Upload complete! Use MySQL Workbench or Power BI to connect.")
    print(f"   Host: {DB_CONFIG['host']} | DB: {DB_CONFIG['database']}")


if __name__ == "__main__":
    run_upload()
