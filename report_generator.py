from jinja2 import Environment, FileSystemLoader
import os

def generate_html_report(summary_text, output_path="report_html/final_report.html"):
    try:
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('report_template.html')

        rendered_html = template.render(
            report_title="SmartFile AI - Python File Summary & Query",
            report_summary=summary_text
        )

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)

        print(f"✅ HTML report generated at: {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Failed to generate HTML report: {e}")
        return None
