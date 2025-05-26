FROM python:3.13.3

LABEL authors="Lilith_Milante"

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y q-text-as-data

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD ["gunicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]