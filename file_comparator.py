import pandas as pd

def compare_csvs(api_csv_path, web_csv_path):
    try:
        api_df = pd.read_csv(api_csv_path)
        web_df = pd.read_csv(web_csv_path)

        # Clean column headers
        api_df.columns = api_df.columns.str.strip().str.lower()
        web_df.columns = web_df.columns.str.strip().str.lower()

        # Check for empty files
        if api_df.empty or web_df.empty:
            return {"error": "One or both CSV files are empty."}

        # Check common columns
        common_cols = list(set(api_df.columns) & set(web_df.columns))

        if not common_cols:
            return {"error": "No common columns found between API and Web files."}

        # Compare shape
        shape_diff = f"API shape: {api_df.shape}, Web shape: {web_df.shape}"
        unique_to_api = list(set(api_df.columns) - set(web_df.columns))
        unique_to_web = list(set(web_df.columns) - set(api_df.columns))

        # Merge safely on common columns
        merged_df = pd.merge(api_df, web_df, how="outer", on=common_cols, indicator=True)

        summary = {
            "shape_diff": shape_diff,
            "common_columns": common_cols,
            "unique_to_api": unique_to_api,
            "unique_to_web": unique_to_web,
            "rows_in_both": int((merged_df["_merge"] == "both").sum()),
            "rows_only_in_api": int((merged_df["_merge"] == "left_only").sum()),
            "rows_only_in_web": int((merged_df["_merge"] == "right_only").sum())
        }

        return summary

    except Exception as e:
        return {"error": f"Comparison failed: {str(e)}"}
