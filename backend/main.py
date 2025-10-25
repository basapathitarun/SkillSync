
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from src.routes import router





def create_app() -> FastAPI:
    """Initialize FastAPI app with routers and configs."""
    app = FastAPI(
        title="Resume Matcher API",
        description="LLM-powered resume-job matching service",
        version="0.1.0",
        debug=True
    )
    load_dotenv()
    
    # include routes from api.py
    app.include_router(router, prefix="/api", tags=["matcher"])

    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

app = create_app()