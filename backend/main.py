from . import routers
from fastapi import FastAPI

app = FastAPI()

app.include_router(routers.router)

