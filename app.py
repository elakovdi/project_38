from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import csv
from collections import Counter
app = Flask(__name__)
app.secret_key = "secret_key"
app.config["UPLOAD_FOLDER"] = "uploads"
def start_csv_sort(file_path):
    data = []
    with open(file_path, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for row in reader:
            director = row[6].strip()
            if director == "Lelouch, Claude":
                data.append(row)
    return data
@app.route("/", methods=["GET", "POST"])
def index():
    data = []
    success_message = None
    error_message = None
    chart_data = None
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".csv"):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            data = process_csv(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            success_message = "File uploaded successfully!"
            years = [row[0] for row in data]
            count_by_year = dict(Counter(years))
            chart_data = {
                "labels": list(count_by_year.keys()),
                "data": list(count_by_year.values())
            }
        else:
            error_message = "Invalid file format! Please upload the CSV file."
    example_data = [
        ["1979","122","Cuba","","","Adams, Brooke", ""],
        ["1978","94","Days of Heaven","","","Adams, Brooke", ""],
        ["1983","140","Octopussy","","","Adams, Maud",""],
    ]
    example_chart_data = {
        "labels": ["1978", "1979", "1983"],
        "data": [1, 1, 1]
    }
    if not data:
        data = example_data
        chart_data = example_chart_data
    return render_template("index.html", data=data, success_message=success_message, error_message=error_message, chart_data=chart_data)
if __name__ == "__main__":
    app.run()
