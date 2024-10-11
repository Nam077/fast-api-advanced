from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
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
            openapi_tags=tags_metadata
        )
        self._register_controllers()
        self._register_exception_handlers()  # Đăng ký handler cho exception

    def _register_controllers(self):
        user_controller = UserController()
        self.app.include_router(user_controller.router, tags=["Users"])

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

    def get_app(self):
        return self.app
