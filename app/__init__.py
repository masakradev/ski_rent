from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app.api import bp as api_bp, routes
app.register_blueprint(api_bp, url_prefix='/api')

from app.dashboard import bp as dashboard_bp, routes
app.register_blueprint(dashboard_bp)