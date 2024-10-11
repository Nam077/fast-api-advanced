from fastapi import FastAPI
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

    def _register_controllers(self):
        user_controller = UserController()
        self.app.include_router(user_controller.router, tags=["Users"], )

    def get_app(self):
        return self.app
