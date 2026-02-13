import matplotlib.pyplot as plt
import seaborn as sns

def revenue_by_city(df):

    city_revenue = (
        df.groupby("City")["Order_Value"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nTop 5 Cities by Revenue:")
    print(city_revenue.head())

    city_revenue.head(10).plot(kind="bar", figsize=(10,5))
    plt.title("Top 10 Cities by Revenue")
    plt.ylabel("Total Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def avg_delivery_time(df):

    avg_time = (
        df.groupby("City")["Delivery_Time_Min"]
        .mean()
        .sort_values(ascending=False)
    )

    print("\nAverage Delivery Time by City:")
    print(avg_time.head())
