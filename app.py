import pandas as pd
from dash import Dash, Input, Output, dcc, html


data = (
    pd.read_csv("weather.csv")
    # .query("Location == 'Dallas'")
    .assign(Date=lambda data: pd.to_datetime(data["Time"], format="%H:%M:%S"))
    .sort_values(by="Time")
)
regions = data["Location"].sort_values().unique()
temp_types = data["Weather"].sort_values().unique()


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
                html.H1(children="Temp Analytics", className="header-title",),
                html.P(children=("Analyze the temp in cities over time"), className="header-title",),
            ], className="header",
        ),

        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Location", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in regions
                            ],
                            value="Dallas",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {
                                    "label": temp_type.title(),
                                    "value": temp_type,
                                }
                                for temp_type in temp_types
                            ],
                            value="clear sky",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Time Range", className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data["Time"].min(),
                            max_date_allowed=data["Time"].max(),
                            start_date=data["Time"].min(),
                            end_date=data["Time"].max(),
                        ),
                    ]
                ),
            ], className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper"
        ),
    ]
)

@app.callback(
    Output("price-chart", "figure"),
    Output("volume-chart", "figure"),
    Input("region-filter", "value"),
    Input("type-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_charts(region, avocado_type, start_date, end_date):
    filtered_data = data.query(
        "region == @region and type == @avocado_type"
        " and Date >= @start_date and Date <= @end_date"
    )
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Time"],
                "y": filtered_data["Temperature"],
                "type": "lines",
                "hovertemplate": "%{y:.2f} C<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Temperature",
                "x": 1,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Time"],
                "y": filtered_data["Humidity"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Humidity", "x": 1, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return price_chart_figure, volume_chart_figure

if __name__ == "__main__":
    app.run_server(debug=True)