from fastapi import FastAPI
from endpoints import router as endpoints_router
import os

app = FastAPI(
    title="William Fitzjohn's PDFTools",
    description="An API for manipulating PDFs.",
    version="1.0.0",
    docs_url=os.environ.get("BASE_URL", "") + "/docs",
    openapi_url=os.environ.get("BASE_URL", "") + "/openapi.json",
)

# Include the endpoints defined in endpoints.py
app.include_router(endpoints_router, prefix=os.environ.get("BASE_URL", ""))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8084)
