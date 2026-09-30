from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.analysis import router as analysis_router
from routes.comparison import router as comparison_router
from routes.product import router as product_router

app = FastAPI(
    title="SmartBuy AI",
    description="AI-powered product comparison platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis_router, prefix="/api")
app.include_router(comparison_router, prefix="/api")
app.include_router(product_router, prefix="/api")


@app.get("/")
def home():
    return {
        "message": "SmartBuy AI Backend is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }