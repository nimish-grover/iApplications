from flask import flash, redirect, render_template, request, session, url_for
from flask_smorest import Blueprint
import plotly.graph_objs as go
import plotly.io as pio
from iLand.app.models.wl_area import WL_Area

def create_state_wise_plot():
    categories = []
    values = []
    data = WL_Area.get_area_state_wise()
    for item in data:
        categories.append(item[0].title())
        values.append(item[1])


    # Create Plotly figure
    fig = go.Figure(data=[go.Bar(x=values, y=categories, orientation='h')])
    fig.update_layout(
        title='Horizontal Bar Chart',
        xaxis=dict(title='Values'),
        yaxis=dict(title='Categories'),
        margin=dict(l=100, r=100, t=50, b=50)
    )

    # Save the plot as an image file
    pio.write_image(fig, 'horizontal_bar_chart.png')

blp = Blueprint("state_wise", "state_wise","state wise waste land area ")

@blp.route('/state_wise_area')
def state_wise_area():
    create_state_wise_plot()
    return render_template('state_wise.html')