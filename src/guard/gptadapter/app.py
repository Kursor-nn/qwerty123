import uvicorn
from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator

from common_consts import RABBIT_HOST, RABBIT_PORT, RABBIT_USER, RABBIT_PASSWORD, GPT_ADAPTER_QUEUE
from core.queue.rmworkers import run_adapter_queue_channel
from core.routes.api_gpt import llm_api_router

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

app.include_router(llm_api_router, prefix="/api/llm")


@app.on_event("startup")
async def _startup():
    instrumentator.expose(app)


if __name__ == "__main__":
    queue = config(GPT_ADAPTER_QUEUE)
    logger.info(f"Start GPT Adapter Worker for {queue}")
    run_adapter_queue_channel(config(RABBIT_HOST),
                              config(RABBIT_PORT),
                              config(RABBIT_USER),
                              config(RABBIT_PASSWORD),
                              queue)
    logger.info(f"Start Rest Adapter Worker for {queue}")
    uvicorn.run("app:app", host="0.0.0.0", port=8081, reload=True)
