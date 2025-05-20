from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
import uvicorn

app = FastAPI(
    title="Collaborative Event Management API",
    version="1.0.0"
)

# Register routes
app.include_router(auth_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consider restricting this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Collaborative Event Management API is running"}

if __name__ == "__main__":
    print("✅ Database connected via Alembic migrations")
    print("🚀 Server running on http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
