from fastapi import FastAPI

from backend.services.bias import router as bias_router
from backend.services.dedup import router as dedup_router
from backend.services.extract import router as extract_router
from backend.services.queries import router as queries_router
from backend.services.retrieval import router as retrieval_router
from backend.services.summarize import router as summarize_router
from backend.services.topics import router as topics_router
from backend.services.perspectives import router as perspectives_router

app = FastAPI()

app.include_router(topics_router, prefix="/topics", tags=["topics"])
app.include_router(queries_router, prefix="/queries", tags=["queries"])
app.include_router(retrieval_router, prefix="/search", tags=["search"])
app.include_router(dedup_router, prefix="/dedup", tags=["dedup"])
app.include_router(extract_router, prefix="/extract", tags=["extract"])
app.include_router(summarize_router, prefix="/summarize", tags=["summarize"])
app.include_router(bias_router, prefix="/bias", tags=["bias"])
app.include_router(
    perspectives_router,
    prefix="/v1/perspectives",
    tags=["perspectives"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
