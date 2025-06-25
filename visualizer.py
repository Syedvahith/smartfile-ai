import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')


def generate_visuals(csv_path, output_name):
    try:
        df = pd.read_csv(csv_path)

        # Pick numeric columns or summary column for chart
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        if not numeric_cols:
            print("No numeric columns found for chart.")
            return None

        plt.figure(figsize=(10, 6))
        df[numeric_cols].sum().plot(kind='bar')
        plt.title(f"Summary of {output_name.replace('_', ' ').title()}")
        plt.tight_layout()

        # Save to static folder
        os.makedirs("static", exist_ok=True)
        img_path = f"static/{output_name}.png"
        plt.savefig(img_path)
        plt.close()

        print(f"📊 Chart saved at: {img_path}")
        return img_path

    except Exception as e:
        print(f"❌ Error generating chart: {e}")
        return None
