import pandas as pd
from dash import Dash, Input, Output, dcc, html


data = (
    pd.read_csv("weather.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"]))
    .sort_values(by="Time")
)
regions = data["Location"].sort_values().unique()


external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Temp Analytics", className="header-title"),
                html.P(
                    children="Analyze the temp in cities over time",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="City", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in regions
                            ],
                            value=regions[0],
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Time Range", className="menu-title"),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data["Date"].min(),
                            max_date_allowed=data["Date"].max(),
                            start_date=data["Date"].min(),
                            end_date=data["Date"].max(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="weather-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("weather-chart", "figure"),
    Input("region-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_charts(region, start_date, end_date):
    filtered_data = data.query(
        "Location == @region and Date >= @start_date and Date <= @end_date"
    )
    figure = {
        "data": [
            {
                "x": filtered_data["Time"],
                "y": filtered_data["Temperature"],
                "type": "lines",
                "name": "Temperature",
                "yaxis": "y1",
                "hovertemplate": "%{y:.2f} °C<extra></extra>",
                "line": {"color": "#17B897"},
            },
            {
                "x": filtered_data["Time"],
                "y": filtered_data["Humidity"],
                "type": "lines",
                "name": "Humidity",
                "yaxis": "y2",
                "hovertemplate": "%{y}%<extra></extra>",
                "line": {"color": "#E12D39"},
            },
        ],
        "layout": {
            "title": {"text": "Temperature & Humidity", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"ticksuffix": " °C", "fixedrange": True, "title": "Temperature"},
            "yaxis2": {
                "ticksuffix": "%",
                "fixedrange": True,
                "title": "Humidity",
                "overlaying": "y",
                "side": "right",
            },
            "legend": {"x": 0, "y": 1.1, "orientation": "h"},
            "hovermode": "x unified",
        },
    }
    return figure


if __name__ == "__main__":
    app.run_server(debug=True)
