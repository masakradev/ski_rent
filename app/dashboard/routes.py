from flask import render_template, flash
from app.dashboard import bp

@bp.route('/')
def index():
    return render_template('index.html')