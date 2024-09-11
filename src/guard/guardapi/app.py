import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from loguru import logger

from core.routes.messages import message_router

app = FastAPI()
instrumentator = Instrumentator().instrument(app)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(message_router, prefix="/api/guard")


@app.on_event("startup")
async def _startup():
    instrumentator.expose(app)


if __name__ == "__main__":
    logger.info("Start Guard API Service")
    uvicorn.run("app:app", host="0.0.0.0", port=8081, reload=True)
