
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.oee_routes import router as oee_router
from app.api.anomaly_routes import router as anomaly_router
from app.api.copilot import router as copilot_router

app = FastAPI(
    title="Manufacturing OEE Analytics System",
    description="AI-powered manufacturing monitoring and predictive analytics",
    version="1.0.0"
)

# Allow the Next.js frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(oee_router)
app.include_router(anomaly_router)
app.include_router(copilot_router)

@app.get("/")
def home():
    return {
        "message": "Manufacturing OEE Analytics System",
        "status": "Running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "Manufacturing OEE System"
    }
