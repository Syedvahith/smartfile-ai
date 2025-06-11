import os
import requests

def download_csv_from_api(output_dir="input_data/api"):
    os.makedirs(output_dir, exist_ok=True)

    url = "https://people.sc.fsu.edu/~jburkardt/data/csv/hw_200.csv"
  # ✅ simple public CSV
    filename = "sample_from_api.csv"
    save_path = os.path.join(output_dir, filename)

    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(save_path, "wb") as f:
            f.write(response.content)

        print(f"[API] CSV downloaded to: {save_path}")
    except Exception as e:
        print(f"[API] Failed to download CSV: {e}")
