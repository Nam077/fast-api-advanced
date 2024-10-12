from typing import AsyncGenerator
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Request, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.db import database
from app.modules.users.controllers.user_controller import UserController

tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users. You can **create**, **read**, **update**, and **delete** users.",
    }
]


class Application:
    def __init__(self):
        self.app = FastAPI(
            title="FastAPI",
            description="FastAPI demo project",
            version="0.1.0",
            openapi_tags=tags_metadata,
            lifespan=self.lifespan_context
        )
        self.scheduler = BackgroundScheduler()
        self.user_controller = UserController()  # Đặt UserController thành một thuộc tính của Application
        self._register_controllers()
        self._register_exception_handlers()

    def _register_controllers(self):
        self.app.include_router(self.user_controller.router, tags=["Users"])  # Sử dụng self.user_controller

    def _register_exception_handlers(self):
        @self.app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            error_messages = [f"{error['loc'][-1]}: {error['msg']}" for error in exc.errors()]
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "message": "Validation error",
                    "details": error_messages,
                },
            )

    def scheduled_task(self):
        self.user_controller.key_service.auto_key_rotation(next(database.get_db()))

    @asynccontextmanager
    async def lifespan_context(self, app: FastAPI) -> AsyncGenerator[None, None]:
        self.scheduler.add_job(self.scheduled_task, "cron", hour=0, minute=0, day="1")
        self.scheduler.start()
        yield
        print("Application shutdown")
        self.scheduler.shutdown()
        pass

    def get_app(self):
        return self.app
