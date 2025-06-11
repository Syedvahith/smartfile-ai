import pandas as pd
import requests
import os

def generate_summary(file_path):
    try:
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"

        df = pd.read_csv(file_path, header=None)

        if df.empty:
            return "The file is empty, no data to summarize."

        # Rename columns for clarity
        df.columns = [f"Column_{i+1}" for i in range(df.shape[1])]

        # Create a readable sample for the LLM
        sample_data = df.head(min(10, len(df))).to_string(index=False)

        # Add basic stats to help the model
        summary_info = f"""
Data Summary:
- Total Rows: {len(df)}
- Total Columns: {df.shape[1]}
"""

        # Build a better prompt
        prompt = f"""
You are a smart data analyst helping summarize tabular data related to damage claims and regional processing information.

Below is a sample of the dataset:
{sample_data}

{summary_info}

Based on this data sample, generate a short, clear summary that describes:
- The structure of the table
- Any noticeable patterns or values
- If possible, mention frequent codes, regions, or statuses

Your summary:
"""

        # Send to Ollama
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "tinyllama",  # or "llama3", or "mistral"
            "prompt": prompt,
            "stream": False
        })

        return response.json()["response"].strip()

    except Exception as e:
        return f"Error generating summary: {e}"
