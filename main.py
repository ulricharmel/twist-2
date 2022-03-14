import os
import pathlib
from pyexpat import features
import numpy as np
import datetime as dt
import dash
# import dash_core_components as dcc
# import dash_html_components as html

from dash import dcc
from dash import html

from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import plotly.express as px

from scipy.stats import rayleigh
from db.api import get_data, get_drop_down, get_timestamp

from model.machine_learning import load_model, predict

# Load the dataset
# avocado = pd.read_csv('avocado-updated-2020.csv')

model = load_model()

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

# Create the Dash app
app = dash.Dash()

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

features = ['AccelerationX', 'AccelerationY', 'AccelerationZ', 'MagneticFieldX',
       'MagneticFieldY', 'MagneticFieldZ', 'X-AxisAngle(Pitch)',
       'Y-AxisAngle(Roll)', 'GyroX', 'GyroY', 'GyroZ']

target = "Z-AxisAgle(Azimuth)"

# Set up the app layout
app.layout = html.Div(children=[
    html.H1(children='Smartphone sensor Dashboard', style={'textAlign': 'center', 'color':'red'}),
    dcc.Dropdown(id='geo-dropdown',
                 options=[{'label': i, 'value': i}
                          for i in features],
                 value=features[0]),
    dcc.Graph(id='Azimuth',
    figure=dict(
        layout=dict(
                    plot_bgcolor=app_color["graph_bg"],
                    paper_bgcolor=app_color["graph_bg"],
                    )
                ),),
    # wind speed
    html.Div(
        [
            html.Div(
                [html.H6("Model", className="graph__title")]
            ),
            dcc.Graph(
                id="prediction",
                figure=dict(
                    layout=dict(
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                    )
                ),
            ),
            dcc.Interval(
                id="id-update",
                interval=int(GRAPH_INTERVAL),
                n_intervals=0,
            ),
        ],
        # className="two-thirds column wind__speed__container",
    ),
])


# Set up the callback function
@app.callback(
    Output(component_id='Azimuth', component_property='figure'),
    Input(component_id='geo-dropdown', component_property='value')
)
def update_graph(selected_geography):
    filtered_avocado = get_drop_down(selected_geography)
    line_fig = px.scatter(filtered_avocado,
                       x=selected_geography, y=target,
                    #    color='green',
                       title=f'Azimuth vs {selected_geography}')
    return line_fig

def get_current_time(nrows=646):
    """ Helper function to get the current time in seconds. """

    # now = dt.datetime.now()
    # total_time = (now.hour * 3600) + (now.minute * 60) + (now.second)

    total_time = np.random.randint(nrows)

    return total_time


@app.callback(
    Output(component_id="prediction", component_property="figure"), Input(component_id="id-update", component_property='n_intervals')
)
def gen_plot(interval):
    """
    Generate the plot graph.

    :params interval: update the graph based on an interval
    """

    time_id = get_current_time()
    start, end = get_timestamp(time_id)
    
    df = get_data(start, end)
    yval, ypred = predict(model, df)
    yval = (yval - yval.mean())/yval.std()
    ypred = (ypred - ypred.mean())/ypred.std()

    true = dict(
        type="scatter",
        y=yval,
        line={"color": "white"},
        hoverinfo="skip",
        mode="lines",
    )
    
    predicted = dict(
        type="scatter",
        y=ypred,
        line={"color": "red"},
        hoverinfo="skip",
        mode="lines",
    )

    layout = dict(
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#fff"},
        height=500,
        xaxis={
            # "range": [0, 200],
            "showline": True,
            "zeroline": False,
            "fixedrange": True,
            # "tickvals": [0, 50, 100, 150, 200],
            # "ticktext": ["0", "50", "100", "150", "200"],
            "title": "Time Elapsed (sec)",
        },
        yaxis={
            # "range": [
            #     min(0, min(df["cons.conf.idx"])),
            #     max(df["cons.conf.idx"]),
            # ],
            "showgrid": True,
            "showline": True,
            "fixedrange": True,
            "zeroline": False,
            "gridcolor": app_color["graph_line"],
            # "nticks": max(6, round(df["cons.conf.idx"].iloc[-1] / 10)),
        },
    )

    return dict(data=[true, predicted], layout=layout)

# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)