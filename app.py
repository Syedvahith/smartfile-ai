from flask import Flask, request, jsonify, render_template
from ai_summary import generate_summary
from question_answering import answer_question
from main import process_pipeline
import os
import glob

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
    api_file, web_file = process_pipeline()

    summaries["api"] = (
        generate_summary(api_file) if api_file and os.path.exists(api_file)
        else "API CSV not available."
    )
    summaries["web"] = (
        generate_summary(web_file) if web_file and os.path.exists(web_file)
        else "Web CSV not available."
    )

    return jsonify({"message": "Summaries generated."})

@app.route("/summaries")
def get_summaries():
    return jsonify({
        "api_summary": summaries["api"],
        "web_summary": summaries["web"]
    })

@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()
    question = data.get("question", "")
    file_type = data.get("file", "api")

    # ✅ Use correct cleaned file paths
    file_path = (
        "output_reports/api/clear_api.csv" if file_type == "api"
        else "output_reports/web/clear_web.csv"
    )

    if not os.path.exists(file_path):
        return jsonify({"answer": "Selected file not found."})

    answer = answer_question(file_path, question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
