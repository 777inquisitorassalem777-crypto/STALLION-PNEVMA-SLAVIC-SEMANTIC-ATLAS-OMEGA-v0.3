FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY stallion ./stallion
COPY tests ./tests
COPY pyproject.toml README.md ./
CMD ["uvicorn", "stallion.api:app", "--host", "0.0.0.0", "--port", "8000"]
