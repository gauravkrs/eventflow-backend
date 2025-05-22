from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.routers.event import router as event_router
from app.routers.collaboration import router as collab_router
from app.routers.event_version import router as event_version_router
import uvicorn

app = FastAPI(
    title="Collaborative Event Management API",
    version="1.0.0"
)

# Register routes
app.include_router(auth_router)
app.include_router(event_router)
app.include_router(collab_router)
app.include_router(event_version_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Collaborative Event Management API is running"}

if __name__ == "__main__":
    print("Database connected")
    print("Server running on http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
