
# syntax=docker/dockerfile:1
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# system deps
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# copy app
COPY . /app

# expose metrics and app port
ENV PORT=8000
EXPOSE 8000

# default command: run kill-switch FastAPI (which also exposes metrics)
CMD ["uvicorn", "services.kill_switch:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
