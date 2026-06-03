from flask import Flask, Response, send_file
import csv
import os
import matplotlib.pyplot as plt

app = Flask(__name__)

CSV_FILE = "medicine_log.csv"
CHART_FILE = "medicine_adherence_chart.png"

def read_log():
    rows = []
    taken = 0
    missed = 0
    no_response = 0

    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                if len(row) == 5:
                    rows.append(row)
                    status = row[4]

                    if status == "taken":
                        taken += 1
                    elif status == "missed":
                        missed += 1
                    elif status == "no_response":
                        no_response += 1

    return rows, taken, missed, no_response

def generate_chart():
    rows, taken, missed, no_response = read_log()

    labels = ["Taken", "Missed", "No Response"]
    values = [taken, missed, no_response]

    plt.figure(figsize=(7, 5))
    plt.bar(labels, values)
    plt.title("Medication Adherence Summary")
    plt.xlabel("Dose Status")
    plt.ylabel("Number of Events")
    plt.tight_layout()
    plt.savefig(CHART_FILE)
    plt.close()

@app.route("/")
def dashboard():
    rows, taken, missed, no_response = read_log()
    generate_chart()

    table_rows = ""

    for row in rows:
        table_rows += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>{row[3]}</td>
            <td>{row[4]}</td>
        </tr>
        """

    html = f"""
    <html>
    <head>
        <title>Medication Dashboard</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body {{
                font-family: Arial;
                background-color: #f4f6f8;
                margin: 30px;
            }}
            h1 {{
                color: #2c3e50;
            }}
            .card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
            }}
            .summary {{
                display: flex;
                gap: 20px;
            }}
            .box {{
                background: #e8f0fe;
                padding: 15px;
                border-radius: 8px;
                width: 180px;
                text-align: center;
                font-size: 18px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 10px;
                text-align: center;
            }}
            th {{
                background-color: #2c3e50;
                color: white;
            }}
            a.button {{
                display: inline-block;
                background-color: #2c3e50;
                color: white;
                padding: 10px 15px;
                margin-right: 10px;
                text-decoration: none;
                border-radius: 5px;
            }}
        </style>
    </head>

    <body>
        <h1>Smart Medication Reminder Dashboard</h1>

        <div class="card">
            <h2>Adherence Summary</h2>
            <div class="summary">
                <div class="box">Taken<br><b>{taken}</b></div>
                <div class="box">Missed<br><b>{missed}</b></div>
                <div class="box">No Response<br><b>{no_response}</b></div>
            </div>
        </div>

        <div class="card">
            <h2>Downloads</h2>
            <a class="button" href="/download_csv">Download CSV</a>
            <a class="button" href="/chart">View Graph</a>
            <a class="button" href="/download_chart">Download Graph</a>
        </div>

        <div class="card">
            <h2>Medication Log</h2>
            <table>
                <tr>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Patient</th>
                    <th>Dose</th>
                    <th>Status</th>
                </tr>
                {table_rows}
            </table>
        </div>

        <div class="card">
            <p>This dashboard updates automatically every 5 seconds.</p>
        </div>
    </body>
    </html>
    """

    return html

@app.route("/download_csv")
def download_csv():
    return send_file(CSV_FILE, as_attachment=True)

@app.route("/chart")
def chart():
    generate_chart()
    return send_file(CHART_FILE, mimetype="image/png")

@app.route("/download_chart")
def download_chart():
    generate_chart()
    return send_file(CHART_FILE, as_attachment=True)

app.run(host="0.0.0.0", port=5000)
