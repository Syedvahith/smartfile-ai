import zipfile
import os
import glob

def extract_zip_and_get_csv(folder):
    zip_files = glob.glob(os.path.join(folder, "*.zip"))
    if not zip_files:
        print("[Extractor] No ZIP files found.")
        return None

    zip_path = zip_files[0]
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(folder)
        print(f"[Extractor] Extracting ZIP: {zip_path}")

    # ✅ Search recursively for .csv
    csv_files = glob.glob(os.path.join(folder, "**", "*.csv"), recursive=True)
    if csv_files:
        print(f"[Extractor] CSV found: {csv_files[0]}")
        return csv_files[0]
    else:
        print("[Extractor] No CSV found after extraction.")
        return None
