from sqlalchemy import create_engine

def connect_db():
    engine = create_engine(
        "mysql+mysqlconnector://root:Test%40123@localhost/food_delivery_db"
    )
    return engine

def upload_to_mysql(df):
    engine = connect_db()
    df.to_sql("orders", con=engine, if_exists="replace", index=False)
    print("Data Uploaded Successfully")
