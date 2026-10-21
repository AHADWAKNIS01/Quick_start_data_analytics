# QuickCart Analytics

QuickCart Analytics is a batch grocery analytics dashboard built from the Instacart Online Grocery Shopping Dataset 2017. Apache Spark (PySpark) reads the CSV tables, creates Parquet aggregates, and publishes the same aggregates to Couchbase. FastAPI reads Couchbase, and a React + TypeScript + Vite dashboard renders the API responses.

This is an analytics product only: there is no shopping cart, checkout, payment, delivery, or order placement flow. Batch output is labelled `sample` or `full`; it is not real time.

## Tested versions

- Apache Spark / PySpark 3.5.8, Java 17, Python 3.11
- Couchbase Server 7.6 (Docker image `couchbase/server:community-7.6.0`), Python SDK 4.3.6
- FastAPI 0.115.6, Uvicorn 0.34.0
- Node 24.14, React 19, Vite 6.3.5, Recharts 2.15.1

Spark 3.5.8 supports Java 8/11/17 and Python 3.8+; Vite's current guide requires Node 20.19+ or 22.12+. The official Instacart download may require account/Kaggle access. The included sample is reproducible and uses the identical pipeline.

## Quick start (sample)

1. Install Docker Desktop (WSL2/Linux), Java 17, Python 3.11, and Node 20+.
2. Start Couchbase and create its bucket:

```bash
docker compose up -d couchbase
python scripts/init_couchbase.py
```

3. Install Python dependencies and run the sample Spark batch. This writes `data/processed/*.parquet` and upserts documents into Couchbase:

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r backend/requirements.txt
python spark_job/etl.py --mode sample --input data/sample --output data/processed --publish couchbase
```

4. Start the API and frontend in separate terminals:

```bash
uvicorn backend.app.main:app --reload --port 8000
cd frontend && npm install && npm run dev
```

Open http://localhost:5173. API docs are at http://localhost:8000/docs.

## Full dataset

Download the Instacart Market Basket / Online Grocery Shopping Dataset 2017 from the official Instacart page or Kaggle, accept any required terms, and extract its CSV files into `data/full/` (`orders.csv`, `order_products__prior.csv`, `order_products__train.csv`, `products.csv`, and optionally `aisles.csv`, `departments.csv`). Then run:

```bash
python spark_job/etl.py --mode full --input data/full --output data/processed --publish couchbase
```

The dashboard's dataset badge changes to `FULL`. The same command works with the small sample by changing `--mode sample`.

## Docker Compose

`docker compose up -d` starts Couchbase and the API (the API waits for Couchbase). The Spark job is intentionally a one-time host/WSL command so students can inspect its logs and rerun it without a cluster. Run the frontend with `npm run dev` or build it with `npm run build`.

For debugging, run each component individually: `python spark_job/etl.py ...`, `uvicorn backend.app.main:app --reload`, and `npm run dev` in `frontend`. Set `COUCHBASE_CONNSTR`, `COUCHBASE_USER`, `COUCHBASE_PASSWORD`, and `COUCHBASE_BUCKET` to override defaults.

## Data model

Couchbase bucket `quickcart` contains documents `quickcart::metadata`, `quickcart::kpis`, `quickcart::hourly`, `quickcart::days`, `quickcart::departments`, and `quickcart::products`. Parquet mirrors each aggregate under `data/processed/`. The API exposes `/api/health`, `/api/summary`, and `/api/analytics/*`.
