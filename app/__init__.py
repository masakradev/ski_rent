from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app.dashboard import bp as dashboard_bp, routes
app.register_blueprint(dashboard_bp)

from app.admin import bp as admin_bp, routes
app.register_blueprint(admin_bp, url_prefix='/admin')