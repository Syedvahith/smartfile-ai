from flask import Flask, request, jsonify, render_template
from ai_summary import generate_summary
from question_answering import answer_question
from main import process_pipeline
import os
import glob
from file_comparator import compare_csvs
from werkzeug.utils import secure_filename



app = Flask(__name__)

summaries = {
    "api": "",
    "web": ""
}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    api_file, web_file, api_chart, web_chart = process_pipeline()

    summaries["api"] = (
        generate_summary(api_file) if api_file and os.path.exists(api_file)
        else "API CSV not available."
    )
    summaries["web"] = (
        generate_summary(web_file) if web_file and os.path.exists(web_file)
        else "Web CSV not available."
    )

    # Store chart paths to send to frontend
    return jsonify({
        "message": "Summaries and charts generated.",
        "api_chart": api_chart,
        "web_chart": web_chart
    })


@app.route("/summaries")
def get_summaries():
    return jsonify({
        "api_summary": summaries["api"],
        "web_summary": summaries["web"],
    })

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty file name"}), 400

    filename = secure_filename(file.filename)
    manual_folder = "input_data/manual"
    os.makedirs(manual_folder, exist_ok=True)
    file_path = os.path.join(manual_folder, filename)
    file.save(file_path)

    # Clean the file
    cleaned_path = "output_reports/manual/cleaned_manual.csv"
    os.makedirs("output_reports/manual", exist_ok=True)
    from data_cleaner import clean_damage_claim_csv
    clean_damage_claim_csv(file_path, cleaned_path)

    # Summary + Chart
    from ai_summary import generate_summary
    from visualizer import generate_visuals
    summary = generate_summary(cleaned_path)
    chart_path = generate_visuals(cleaned_path, "bar_chart_manual")

    chart_url = None
    if chart_path and os.path.exists(chart_path):
        static_path = os.path.join("static", "bar_chart_manual.png")
        os.makedirs("static", exist_ok=True)
        import shutil
        shutil.copy(chart_path, static_path)
        chart_url = "/static/bar_chart_manual.png"
    else:
        chart_url = None

    return jsonify({
        "message": "Manual file processed successfully.",
        "summary": summary,
        "chart": chart_url
    })


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    file_type = data.get("file", "api")

    file_path = (
        "output_reports/api/clear_api.csv" if file_type == "api"
        else "output_reports/web/clear_web.csv"
    )

    if not os.path.exists(file_path):
        return jsonify({"answer": "Selected file not found."})

    answer = answer_question(file_path, question)
    return jsonify({"answer": answer, "question": question})

@app.route("/compare", methods=["GET"])
def compare():
    api_csv = "output_reports/api/clear_api.csv"
    web_csv = "output_reports/web/clear_web.csv"

    if not os.path.exists(api_csv) or not os.path.exists(web_csv):
        return jsonify({"error": "Both files must be available for comparison."}), 400

    comparison_result = compare_csvs(api_csv, web_csv)
    return jsonify(comparison_result)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
