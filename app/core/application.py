from fastapi import FastAPI
from app.modules.users.controllers.user_controller import UserController

class Application:
    def __init__(self):
        self.app = FastAPI()
        self._register_controllers()

    def _register_controllers(self):
        user_controller = UserController()
        self.app.include_router(user_controller.router)

    def get_app(self):
        return self.app
