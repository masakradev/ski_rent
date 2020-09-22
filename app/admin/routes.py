from flask import render_template

from app.admin import bp


@bp.route('/cennik')
def cennik():
    return render_template('cennik.html')