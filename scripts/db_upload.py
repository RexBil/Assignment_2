"""
Upload cleaned/featured data to MySQL
Run: python scripts/db_upload.py
"""

import pandas as pd
from sqlalchemy import create_engine, text
import os
import warnings
warnings.filterwarnings('ignore')

# ── UPDATE THESE WITH YOUR MYSQL CREDENTIALS ──────────────────
DB_CONFIG = {
    'host'    : 'localhost',
    'port'    : 3306,
    'user'    : 'root',
    'password': 'Test%40123',   # ← Change this
    'database': 'food_delivery_db'
}

DATA_PATH = "data/cleaned/featured_food_delivery.csv"


def get_engine():
    url = (f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
           f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    return create_engine(url, echo=False)


def create_database(engine):
    # Connect without database first to create it
    root_url = (f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
                f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}")
    root_engine = create_engine(root_url)
    with root_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}"))
        conn.commit()
    print(f"✅ Database '{DB_CONFIG['database']}' ready")


def upload_data():
    print("\n📤 UPLOADING DATA TO MYSQL\n" + "=" * 40)

    df = pd.read_csv(DATA_PATH)

    # Convert Profit_Margin to percentage if stored as fraction
    if df['Profit_Margin'].abs().max() <= 1.5:
        df['Profit_Margin']     = df['Profit_Margin'] * 100
        df['profit_margin_pct'] = df['profit_margin_pct'] * 100

    print(f"Dataset loaded: {df.shape[0]:,} rows, {df.shape[1]} columns")

    create_database(None)
    engine = get_engine()

    # Run schema SQL
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'sql', 'create_tables.sql')
    if os.path.exists(schema_path):
        with open(schema_path) as f:
            sql = f.read()
        with engine.connect() as conn:
            for stmt in sql.split(';'):
                stmt = stmt.strip()
                if stmt and not stmt.startswith('--'):
                    try:
                        conn.execute(text(stmt))
                    except Exception:
                        pass
            conn.commit()
        print("✅ Schema created")

    # Upload data
    df.to_sql('food_orders', con=engine, if_exists='replace',
              index=False, chunksize=5000, method='multi')

    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM food_orders")).scalar()
    print(f"✅ food_orders: {count:,} rows uploaded")
    print(f"\n🎉 Done! Connect MySQL Workbench or Power BI to:")
    print(f"   Host: {DB_CONFIG['host']} | DB: {DB_CONFIG['database']}")


if __name__ == "__main__":
    upload_data()
