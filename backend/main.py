import backend.routers as routers
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

app = FastAPI()

app.include_router(routers.router)
app.add_exception_handler(RequestValidationError,
                          routers.validation_exception_handler)
