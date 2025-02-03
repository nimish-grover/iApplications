from flask import make_response, render_template, request, send_from_directory, g, session
from flask_smorest import Blueprint
from iWater.app.routes.water_budget import WaterBudgetCalc


blp = Blueprint('entry', 'entry', description="data entry routes")

@blp.route('/select_states')
def select_states():
    payload = session.get('payload')
    states = WaterBudgetCalc.get_states()
    return render_template('select_states.html',states = states)