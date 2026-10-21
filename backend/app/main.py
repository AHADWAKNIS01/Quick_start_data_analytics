from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .db import get_doc

app = FastAPI(title="QuickCart Analytics API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_methods=["GET"], allow_headers=["*"])

@app.get("/api/health")
def health():
    try:
        meta = get_doc("quickcart::metadata")
        return {"status": "ok", "dataset": meta.get("dataset"), "generated_at": meta.get("generated_at")}
    except Exception as exc:
        raise HTTPException(503, detail=f"Couchbase unavailable or batch not loaded: {exc}")

def doc(name):
    try: return get_doc(f"quickcart::{name}")
    except Exception as exc: raise HTTPException(503, detail=f"Analytics not loaded: {exc}")

@app.get("/api/summary")
def summary(): return {"metadata": doc("metadata"), "kpis": doc("kpis")}
@app.get("/api/analytics/hourly")
def hourly(): return doc("hourly")
@app.get("/api/analytics/days")
def days(): return doc("days")
@app.get("/api/analytics/departments")
def departments(): return doc("departments")
@app.get("/api/analytics/products")
def products(): return doc("products")
