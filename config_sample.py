import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '983h7s73e1hbns763mc87123'
    APP_NAME = "PamirSki"
    db_name = 'database.db'
    logo = ""