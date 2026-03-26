"""
main.py — Master Pipeline Runner
Online Food Delivery Analysis Project

Usage:
    python main.py --step all
    python main.py --step clean
    python main.py --step features
    python main.py --step eda
    python main.py --step analytics
    python main.py --step upload
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

RAW_PATH      = "data/raw/ONINE_FOOD_DELIVERY_ANALYSIS.csv"
CLEANED_PATH  = "data/cleaned/cleaned_food_delivery.csv"
FEATURED_PATH = "data/cleaned/featured_food_delivery.csv"


def run_all():
    import pandas as pd
    from scripts.data_cleaning       import clean_data
    from scripts.feature_engineering import engineer_features
    from scripts.eda                 import run_eda
    from scripts.analytics           import run_all_analytics

    print("\n🚀 RUNNING FULL PIPELINE\n" + "═" * 55)

    df_clean = clean_data(RAW_PATH, CLEANED_PATH)

    df_feat = engineer_features(df_clean.copy())
    os.makedirs(os.path.dirname(FEATURED_PATH), exist_ok=True)
    df_feat.to_csv(FEATURED_PATH, index=False)
    print(f"💾 Featured data saved: {FEATURED_PATH}")

    run_eda(df_feat)
    run_all_analytics(df_feat)

    print("\n🎉 Pipeline complete!")
    print("   ➡️  Charts saved to: outputs/")
    print("   ➡️  Run dashboard: streamlit run dashboard/app.py")


def main():
    parser = argparse.ArgumentParser(description='Food Delivery Analysis Pipeline')
    parser.add_argument('--step', default='all',
                        choices=['all', 'clean', 'features', 'eda', 'analytics', 'upload'])
    args = parser.parse_args()

    import pandas as pd

    if args.step == 'all':
        run_all()

    elif args.step == 'clean':
        from scripts.data_cleaning import clean_data
        clean_data(RAW_PATH, CLEANED_PATH)

    elif args.step == 'features':
        from scripts.feature_engineering import engineer_features
        df = pd.read_csv(CLEANED_PATH)
        df = engineer_features(df)
        df.to_csv(FEATURED_PATH, index=False)
        print(f"💾 Saved: {FEATURED_PATH}")

    elif args.step == 'eda':
        from scripts.eda import run_eda
        df = pd.read_csv(FEATURED_PATH)
        run_eda(df)

    elif args.step == 'analytics':
        from scripts.analytics import run_all_analytics
        df = pd.read_csv(FEATURED_PATH)
        run_all_analytics(df)

    elif args.step == 'upload':
        from scripts.db_upload import run_upload
        run_upload()


if __name__ == "__main__":
    main()
