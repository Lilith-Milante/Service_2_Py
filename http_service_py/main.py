from flask import Flask, request, jsonify
import subprocess

app = Flask(__name___)

PORT = 3000

@app.route("/query", methods=["POST"])
def query_csv():
    sql = request.json.get("sql")
    if not sql:
        return {"error": "SQL query missing"}, 400

    try:
        # Выполняем команду q через subprocess
        result = subprocess.run(
            ["q", "-H", "--csv", sql],
            cwd="/app",  # где лежит data.csv
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            return {"error": result.stderr.strip()}, 400
        return {"result": result.stdout.strip()}
    except Exception as e:
        return {"error": str(e)}, 500