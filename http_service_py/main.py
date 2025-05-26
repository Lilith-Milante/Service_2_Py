from flask import Flask, request, jsonify, app
from io import StringIO
import subprocess

PORT = 3000

app = Flask(__name__)

# Вспомогательная функция для добавления "FROM -"
def ensure_from_clause(sql: str) -> str:
    sql_upper = sql.upper()
    if "FROM" not in sql_upper:
        if "WHERE" in sql_upper:
            parts = sql.split("WHERE", 1)
            return f"{parts[0].strip()} FROM - WHERE {parts[1].strip()}"
        else:
            return f"{sql.strip()} FROM -"
    return sql

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

    # Добавляем FROM - если его нет
    sql_query = ensure_from_clause(sql_query)

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

        output = result.stdout.decode('utf-8').strip()

        # Парсим результат в список списков
        if not output:
            return jsonify({"result": []})

        rows = [line.split(",") for line in output.splitlines()]
        return jsonify({"result": rows})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)