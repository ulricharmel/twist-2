# Import libraries
import os
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from db.api import get_data
import datetime as dt
import numpy as np

# Load the dataset
avocado = pd.read_csv('avocado-updated-2020.csv')

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

# Create the Dash app
app = dash.Dash()

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

# Set up the app layout
app.layout = html.Div(children=[
    html.H1(children='Avocado Prices Dashboard'),
    dcc.Dropdown(id='geo-dropdown',
                 options=[{'label': i, 'value': i}
                          for i in avocado['geography'].unique()],
                 value='New York'),
    dcc.Graph(id='price-graph',
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
                [html.H6("Cumstomer confidence", className="graph__title")]
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
                id="wind-speed-update",
                interval=int(GRAPH_INTERVAL),
                n_intervals=0,
            ),
        ],
        className="two-thirds column wind__speed__container",
    ),
])


# Set up the callback function
@app.callback(
    Output(component_id='price-graph', component_property='figure'),
    Input(component_id='geo-dropdown', component_property='value')
)
def update_graph(selected_geography):
    filtered_avocado = avocado[avocado['geography'] == selected_geography]
    line_fig = px.line(filtered_avocado,
                       x='date', y='average_price',
                       color='type',
                       title=f'Avocado Prices in {selected_geography}')
    return line_fig

def get_current_time(nrows=41188-200):
    """ Helper function to get the current time in seconds. """

    # now = dt.datetime.now()
    # total_time = (now.hour * 3600) + (now.minute * 60) + (now.second)

    total_time = np.random.randint(nrows)

    return total_time


@app.callback(
    Output(component_id="prediction", component_property="figure"), Input(component_id="wind-speed-update", component_property='n_intervals')
)
def gen_plot(interval):
    """
    Generate the plot graph.

    :params interval: update the graph based on an interval
    """

    total_time = get_current_time()
    df = get_data(total_time - 1000, total_time)

    trace = dict(
        type="scatter",
        y=10*np.sin(df["cons.conf.idx"]),
        line={"color": "#42C4F7"},
        hoverinfo="skip",
        error_y={
            "type": "data",
            "array": 0.005*np.abs(np.sin(df["cons.conf.idx"])),
            "thickness": 1.5,
            "width": 2,
            "color": "#B4E8FC",
        },
        mode="lines",
    )

    layout = dict(
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#fff"},
        height=700,
        xaxis={
            "range": [0, 200],
            "showline": True,
            "zeroline": False,
            "fixedrange": True,
            "tickvals": [0, 50, 100, 150, 200],
            "ticktext": ["0", "50", "100", "150", "200"],
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
            "nticks": max(6, round(df["cons.conf.idx"].iloc[-1] / 10)),
        },
    )

    return dict(data=[trace], layout=layout)

# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)