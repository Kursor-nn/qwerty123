import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database.database import conn
from core.routes.features import features_router
from core.routes.users import user_router

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    conn()


app.include_router(user_router, prefix="/api/user")
app.include_router(features_router, prefix="/api/features")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8081, reload=True)