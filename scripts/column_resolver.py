"""
column_resolver.py
Automatically maps actual dataset column names to logical names
used throughout the project.
"""

import pandas as pd


# ── Keyword patterns for each logical column ──────────────────────────────────
PATTERNS = {
    'order_id'            : ['order_id', 'orderid', 'order_no', 'id'],
    'order_date'          : ['order_date', 'orderdate', 'date', 'order_time', 'ordertime'],
    'customer_id'         : ['customer_id', 'customerid', 'cust_id', 'user_id'],
    'customer_age'        : ['customer_age', 'age'],
    'customer_gender'     : ['gender', 'customer_gender'],
    'city'                : ['city', 'location', 'customer_city', 'order_city'],
    'restaurant_id'       : ['restaurant_id', 'restaurantid', 'rest_id'],
    'restaurant_name'     : ['restaurant_name', 'restaurantname', 'restaurant'],
    'cuisine_type'        : ['cuisine_type', 'cuisine', 'food_type', 'category'],
    'order_value'         : ['order_value', 'order_amount', 'total_amount',
                             'amount', 'total', 'price', 'order_total', 'gmv'],
    'discount_amount'     : ['discount_amount', 'discount', 'coupon_amount',
                             'promo_amount', 'offer_amount'],
    'payment_mode'        : ['payment_mode', 'payment_method', 'payment_type', 'payment'],
    'order_status'        : ['order_status', 'status', 'delivery_status'],
    'cancellation_reason' : ['cancellation_reason', 'cancel_reason', 'reason'],
    'delivery_time'       : ['delivery_time_minutes', 'delivery_time', 'time_taken',
                             'delivery_duration', 'time_minutes'],
    'distance_km'         : ['distance_km', 'distance', 'delivery_distance'],
    'delivery_rating'     : ['delivery_rating', 'rider_rating', 'driver_rating'],
    'restaurant_rating'   : ['restaurant_rating', 'rest_rating', 'food_rating', 'rating'],
    'profit_margin'       : ['profit_margin', 'margin', 'profit_margin_pct',
                             'profit_margin_percentage'],
    'revenue'             : ['revenue', 'net_revenue', 'gross_revenue'],
    'cost'                : ['cost', 'delivery_cost', 'total_cost'],
}


def resolve_columns(df: pd.DataFrame, verbose: bool = True) -> dict:
    """
    Returns a mapping: logical_name -> actual_column_name.
    If a logical column can't be matched, its value is None.
    """
    cols_lower = {c.lower().strip(): c for c in df.columns}
    mapping = {}

    for logical, candidates in PATTERNS.items():
        matched = None
        for candidate in candidates:
            if candidate.lower() in cols_lower:
                matched = cols_lower[candidate.lower()]
                break
        mapping[logical] = matched

    if verbose:
        print("\n📋 Column Mapping (logical → actual)")
        print("─" * 45)
        for k, v in mapping.items():
            status = f"✅ {v}" if v else "❌ not found"
            print(f"  {k:<25} → {status}")
        print()

    return mapping


def get(mapping: dict, logical: str, df: pd.DataFrame = None) -> str | None:
    """
    Return the actual column name for a logical name.
    Optionally validates it exists in df.
    """
    col = mapping.get(logical)
    if col and df is not None and col not in df.columns:
        return None
    return col
