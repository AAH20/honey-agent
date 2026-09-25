FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY honey_agent/ ./honey_agent/
COPY tests/ ./tests/

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["honey-agent"]
CMD ["drill"]
