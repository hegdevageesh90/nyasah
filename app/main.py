from fastapi import FastAPI
from app.routes.review_routes import router as review_router
from app.routes.user_generated_content_routes import router as ugc_router
from app.routes.event_routes import router as event_router
from app.routes.tenant_routes import router as tenant_router

import uvicorn

app = FastAPI()
api_prefix = "/api"

app.include_router(review_router, prefix=api_prefix)
app.include_router(ugc_router, prefix=api_prefix)
app.include_router(event_router, prefix=api_prefix)
app.include_router(tenant_router, prefix=api_prefix)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Social Proofing API!"}


if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=5000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()
