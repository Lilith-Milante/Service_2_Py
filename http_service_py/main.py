from flask import Flask, request, jsonify
import subprocess
import tempfile
import os
import csv

PORT = 3000

app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query_csv():
    file = request.files.get("file")
    sql = request.form.get("sql")

    if not file or not sql:
        return jsonify({"error": "Missing file or SQL query"}), 400

    try:
        # создаём временную директорию
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, file.filename)
            file.save(filepath)

            result = subprocess.run(
                ["q", "-H", "--csv", sql],
                cwd=tmpdir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode != 0:
                return jsonify({"error": result.stderr.strip()}), 400

            # Преобразуем CSV-ответ в список списков
            reader = csv.reader(result.stdout.strip().splitlines())
            data = [row for row in reader]

            return jsonify({"result": data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500