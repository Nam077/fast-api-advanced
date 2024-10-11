# app/main.py
from app.core.application import Application
from app.core.db import database

# Khởi tạo và chạy ứng dụng FastAPI
app = Application().get_app()

# Tạo bảng trong cơ sở dữ liệu
database.create_tables()
