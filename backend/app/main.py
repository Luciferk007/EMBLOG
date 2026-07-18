from fastapi import FastAPI

from app.api.v1.routes.can import router as can_router

app = FastAPI(
    title="Emblog API",
    version="0.1.0"
)


@app.get("/")
def root():
    return {"message": "Welcome to Emblog API"}

app.include_router(can_router)
@app.get("/health")
def health():
    return {"status": "healthy"}