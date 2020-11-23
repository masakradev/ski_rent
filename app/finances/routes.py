from app.finances import bp

from flask import render_template

@bp.route('/rozliczenia')
def rozliczenia():
    return render_template('rozliczenia.html')