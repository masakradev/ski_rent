" app/ main module"
from app.dashboard import bp as dashboard_bp, routes
from app.admin import bp as admin_bp, routes
from app.finances import bp as finances_bp, routes

from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(dashboard_bp)

app.register_blueprint(admin_bp, url_prefix='/admin')

app.register_blueprint(finances_bp, url_prefix='/finances')

