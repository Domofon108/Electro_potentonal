FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .

# We install only the necessary system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc python3-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

COPY . .
CMD ["python", "bot.py"]
