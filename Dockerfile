# Dockerfile — MS-V reproducible simulation environment

FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-lock.txt .
RUN pip install --no-cache-dir -r requirements-lock.txt

COPY . .

ENV PYTHONPATH=/app
ENV OMP_NUM_THREADS=1
ENV OPENBLAS_NUM_THREADS=1

# Default: reproducibility gate
CMD ["python", "-m", "sim.reproduce"]

# Full campaign (override at run):
# docker run --cpus=32 ms-v bash run_all.sh
