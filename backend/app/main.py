from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import transactions_router, limits_router, invoices_router

app = FastAPI(title="Ewidencja3D")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions_router, prefix="/api/transactions")
app.include_router(limits_router, prefix="/api/limits")
app.include_router(invoices_router, prefix="/api/invoices")


@app.get("/api/health")
def health():
    return {"status": "ok"}
