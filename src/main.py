from fastapi import FastAPI
from .routers.compare import router

app = FastAPI()

app.include_router(router)


@app.get("/")
def read_root():
    return {"Hello": "Data discrepancies checker"}
