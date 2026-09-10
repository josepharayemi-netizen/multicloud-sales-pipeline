FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "src.pipeline", "--input", "data/raw/sales.csv", "--output", "data/processed", "--database", "data/sales.db"]
