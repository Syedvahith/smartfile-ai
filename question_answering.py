import pandas as pd
import requests
import re
import os

def run_data_logic(df, question):
    try:
        question = question.lower()

        # 🔸 Row & column count
        if "how many rows" in question:
            return f"The file has {len(df)} rows."
        elif "how many columns" in question:
            return f"The file has {df.shape[1]} columns."

        # 🔸 Column headers
        elif "column" in question and "name" in question or "header" in question:
            return f"File has columns: {', '.join(['Column_' + str(i+1) for i in range(df.shape[1])])}"

        # 🔸 Least / minimum
        elif "least" in question or "minimum" in question:
            col_idx = detect_column_index(question)
            if col_idx < df.shape[1]:
                return f"Minimum value in column {col_idx+1}: {df.iloc[:, col_idx].min()}"
            else:
                return f"Column {col_idx+1} doesn't exist."

        # 🔸 Max / highest
        elif "max" in question or "highest" in question:
            col_idx = detect_column_index(question)
            if col_idx < df.shape[1]:
                return f"Maximum value in column {col_idx+1}: {df.iloc[:, col_idx].max()}"
            else:
                return f"Column {col_idx+1} doesn't exist."

        # 🔸 Average
        elif "average" in question or "mean" in question:
            col_idx = detect_column_index(question)
            if col_idx < df.shape[1]:
                return f"Average value in column {col_idx+1}: {df.iloc[:, col_idx].mean()}"
            else:
                return f"Column {col_idx+1} doesn't exist."

        # 🔸 Sum
        elif "sum" in question or "total" in question:
            col_idx = detect_column_index(question)
            if col_idx < df.shape[1]:
                return f"Total sum in column {col_idx+1}: {df.iloc[:, col_idx].sum()}"
            else:
                return f"Column {col_idx+1} doesn't exist."

        return None  # if no match, fallback to LLM

    except Exception as e:
        return f"Error in logic handler: {e}"


def detect_column_index(question):
    if "first" in question:
        return 0
    elif "second" in question:
        return 1
    elif "third" in question:
        return 2
    else:
        match = re.search(r"column\s*(\d+)", question)
        if match:
            return int(match.group(1)) - 1
    return 0


def run_llm_response(df, question):
    try:
        preview_text = df.head(min(10, len(df))).to_string(index=False)

        prompt = f"""
You are an expert assistant working with tabular CSV data.

Here is a sample of the data:
{preview_text}

Question: {question}
Answer:
"""

        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "tinyllama",  # or "llama3"tinyllama
            "prompt": prompt,
            "stream": False
        })

        return response.json()["response"].strip()

    except Exception as e:
        return f"Error generating AI answer: {e}"


def answer_question(file_path, question):
    try:
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"

        df = pd.read_csv(file_path, header=None)

        logic_answer = run_data_logic(df, question)
        if logic_answer:
            return logic_answer

        return run_llm_response(df, question)

    except Exception as e:
        return f"Error answering question: {e}"
