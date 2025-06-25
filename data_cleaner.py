import pandas as pd
import os
import csv

def clean_damage_claim_csv(input_csv_path, output_csv_path):
    try:
        # df = pd.read_csv(input_csv_path, header=None, engine='python', on_bad_lines='skip', delimiter=',', quoting=csv.QUOTE_MINIMAL)
        try:
            df = pd.read_csv(input_csv_path, encoding="utf-8", header=None, engine='python', on_bad_lines='skip', delimiter=',', quoting=csv.QUOTE_MINIMAL)
        except UnicodeDecodeError:
            df = pd.read_csv(input_csv_path, encoding="ISO-8859-1")  # fallback for non-UTF8 files


        print(f"[Cleaner] Original shape: {df.shape}")

        # Remove 22nd column if it exists
        if df.shape[1] > 21:
            df.drop(df.columns[21], axis=1, inplace=True)
            print("[Cleaner] Removed 22nd column")

        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        df.to_csv(output_csv_path, index=False, header=False)
        print(f"[Cleaner] Cleaned CSV saved at: {output_csv_path}")
        return output_csv_path

    except Exception as e:
        print(f"[Cleaner] Error while cleaning CSV: {e}")
        return None
