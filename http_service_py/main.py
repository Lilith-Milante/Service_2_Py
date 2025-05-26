from flask import Flask, request, jsonify, app
from io import StringIO
import subprocess

PORT = 3000

app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query_csv():
    # Получаем CSV как текст из form-data
    csv_data = request.form.get('csv-text')
    if not csv_data:
        return jsonify({"error": "Missing CSV data"}), 400

    # Получаем SQL-запрос из form-data
    sql_query = request.form.get('sql')
    if not sql_query:
        return jsonify({"error": "Missing SQL query"}), 400

    try:
        # Запускаем q через subprocess, передаём SQL-запрос и CSV через stdin
        result = subprocess.run(
            ['q', '-H', '--delimiter', ',',
             f'{sql_query}'],
            input=csv_data.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode != 0:
            return jsonify({"error": result.stderr.decode('utf-8')}), 400

        output = result.stdout.decode('utf-8')
        return jsonify({"result": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)