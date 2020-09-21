
from app.dashboard import bp

@bp.route('/')
def index():
    return "Test"