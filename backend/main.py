from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.responses import JSONResponse
import backend.routers as routers
from fastapi import FastAPI, Request, status

app = FastAPI()

app.include_router(routers.router)
