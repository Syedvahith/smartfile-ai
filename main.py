
import os
import glob
import shutil
from api_downloader import download_csv_from_api
from web_downloader import download_zip_from_portal
from file_extractor import extract_zip_and_get_csv
from data_cleaner import clean_damage_claim_csv
from ftp_uploader import upload_to_ftp
from visualizer import generate_visuals

def clear_folder(folder):
    """
    Clears all files and subfolders in the given directory.
    """
    for f in os.listdir(folder):
        path = os.path.join(folder, f)
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as e:
            print(f"Error deleting {path}: {e}")

def get_latest_csv(folder):
    """
    Returns the most recently created CSV file in a folder.
    """
    csv_files = glob.glob(os.path.join(folder, "*.csv"))
    if csv_files:
        return max(csv_files, key=os.path.getctime)
    return None

def process_pipeline():
    print("[STEP] Starting full damage claims automation")

    # Step 1: Clear old files from input/output folders
    clear_folder("input_data/api")
    clear_folder("input_data/web")
    clear_folder("output_reports/api")
    clear_folder("output_reports/web")
    clear_folder("static")


    # Step 2: Download API and Web CSV
    download_csv_from_api("input_data/api")
    download_zip_from_portal("input_data/web")
    extracted_csv = extract_zip_and_get_csv("input_data/web")

    # Step 3: Define file paths
    api_csv = get_latest_csv("input_data/api")
    api_clean_path = "output_reports/api/clear_api.csv"
    web_clean_path = "output_reports/web/clear_web.csv"

    # Step 4: Clean and save
    if api_csv:
        clean_damage_claim_csv(api_csv, api_clean_path)
        print(f"[Cleaner] Cleaned API CSV saved at: {api_clean_path}")
    else:
        print("[Pipeline] API CSV not found.")

    if extracted_csv and os.path.exists(extracted_csv):
        clean_damage_claim_csv(extracted_csv, web_clean_path)
        print(f"[Cleaner] Cleaned Web CSV saved at: {web_clean_path}")
    else:
        print("[Pipeline] Web CSV not found.")

    # Step 5: Upload cleaned files to FTP
    if os.path.exists(api_clean_path):
        upload_to_ftp(api_clean_path)
    else:
        print("❌ FTP upload failed: API cleaned file missing.")

    if os.path.exists(web_clean_path):
        upload_to_ftp(web_clean_path)
    else:
        print("❌ FTP upload failed: Web cleaned file missing.")

    # Step 6: Generate visualizations (charts)
    api_chart = generate_visuals(api_clean_path, "bar_chart_api") if os.path.exists(api_clean_path) else None
    web_chart = generate_visuals(web_clean_path, "bar_chart_web") if os.path.exists(web_clean_path) else None

    return api_clean_path, web_clean_path, api_chart, web_chart

# import os
# import glob
# import shutil
# from api_downloader import download_csv_from_api
# from web_downloader import download_zip_from_portal
# from file_extractor import extract_zip_and_get_csv
# from data_cleaner import clean_damage_claim_csv
# from ftp_uploader import upload_to_ftp
# from visualizer import generate_visuals

# def clear_folder(folder):
#     """
#     Clears all files and subfolders in the given directory.
#     """
#     for f in os.listdir(folder):
#         path = os.path.join(folder, f)
#         try:
#             if os.path.isfile(path):
#                 os.remove(path)
#             elif os.path.isdir(path):
#                 shutil.rmtree(path)
#         except Exception as e:
#             print(f"Error deleting {path}: {e}")


# def get_latest_csv(folder):
#     """
#     Returns the most recently created CSV file in a folder.
#     """
#     csv_files = glob.glob(os.path.join(folder, "*.csv"))
#     if csv_files:
#         return max(csv_files, key=os.path.getctime)
#     return None


# def process_pipeline():
#     print("[STEP] Starting full damage claims automation")

#     # Step 1: Clear old files from input/output folders
#     clear_folder("input_data/api")
#     clear_folder("input_data/web")
#     clear_folder("output_reports/api")
#     clear_folder("output_reports/web")

#     # Step 2: Download API CSV to input_data/api
#     download_csv_from_api("input_data/api")

#     # Step 3: Download ZIP file from web and extract CSV to input_data/web
#     download_zip_from_portal("input_data/web")
#     extracted_csv = extract_zip_and_get_csv("input_data/web")  # CSV path from ZIP

#     # Step 4: Define paths
#     api_csv = get_latest_csv("input_data/api")
#     api_clean_path = "output_reports/api/clear_api.csv"
#     web_clean_path = "output_reports/web/clear_web.csv"

#     # Step 5: Clean and save files
#     if api_csv:
#         clean_damage_claim_csv(api_csv, api_clean_path)
#         print(f"[Cleaner] Cleaned API CSV saved at: {api_clean_path}")
#     else:
#         print("[Pipeline] API CSV not found.")

#     if extracted_csv and os.path.exists(extracted_csv):
#         clean_damage_claim_csv(extracted_csv, web_clean_path)
#         print(f"[Cleaner] Cleaned Web CSV saved at: {web_clean_path}")
#     else:
#         print("[Pipeline] Web CSV not found.")

#     # Step 6: Upload to FTP
#     if os.path.exists(api_clean_path):
#         upload_to_ftp(api_clean_path)
#     else:
#         print("❌ FTP upload failed: API cleaned file missing.")

#     if os.path.exists(web_clean_path):
#         upload_to_ftp(web_clean_path)
#     else:
#         print("❌ FTP upload failed: Web cleaned file missing.")

#     # Step 7: Generate charts for visual insights
#     # After cleaning
#     if os.path.exists(api_clean_path):
#         generate_visuals(api_clean_path, "bar_chart_api")

#     if os.path.exists(web_clean_path):
#         generate_visuals(web_clean_path, "bar_chart_web")

#     return api_clean_path, web_clean_path, api_chart, web_chart

