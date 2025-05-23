from flask import Flask, request, jsonify
import subprocess

PORT = 3000

app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query_csv():
    sql = request.json.get("sql")
    if not sql:
        return jsonify({"error": "Missing SQL query"}), 400

    try:
        # Запуск утилиты q
        result = subprocess.run(
            ["q", "-H", "--csv", sql],
            cwd="/app",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return jsonify({"error": result.stderr.strip()}), 400

        return jsonify({"result": result.stdout.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500