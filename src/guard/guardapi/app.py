import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import start_http_server

from core.routes.messages import message_router

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(message_router, prefix="/api/guard")

if __name__ == "__main__":
    start_http_server(8082)
    uvicorn.run("app:app", host="0.0.0.0", port=8081, reload=True)
