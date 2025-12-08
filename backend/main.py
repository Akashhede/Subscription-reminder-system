import sys
import os

# Load environment variables FIRST before any backend imports
# so auth.py and all modules read SECRET_KEY from .env, not the fallback value
from dotenv import load_dotenv
load_dotenv()

# Add the parent directory (project root) to sys.path
# This allows 'from backend...' imports to work regardless of where the script is run from
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import Base, engine
from backend.routes.user_routes import router as user_router
from backend.routes.subscription_routes import router as subscription_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
app = FastAPI(title="Subscription Reminder API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(os.path.join(BASE_DIR, "static", "favicon.ico"), media_type="image/vnd.microsoft.icon")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix="/auth", tags=["auth"])
app.include_router(subscription_router, prefix="/subscription", tags=["subscription"])

@app.get("/")
def root():
    return {"msg":"Subscription Reminder API running"}

@app.on_event("startup")
async def startup_event():
    # Placeholder for startup tasks (e.g., scheduler)
    return None


@app.on_event("shutdown")
async def shutdown_event():
    # Placeholder for shutdown tasks
    return None

