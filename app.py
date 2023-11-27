import pandas as pd
from dash import Dash, Input, Output, dcc, html


data = (
    pd.read_csv("weather.csv")
    .query("Location == 'Dallas'")
    .assign(Date=lambda data: pd.to_datetime(data["Time"], format="%H:%M:%S"))
    .sort_values(by="Time")
)


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

        html.H1(children="Temp Analytics"),
        html.P(children=("Analyze the temp in cities over time"),),

        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Time"],
                        "y": data["Temperature"],
                        "type": "lines",
                        "hovertemplate": ("%{y:.2f}C<extra></extra>")
                    },
                ],
                "layout": {"title": "Average temp changes"}
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Time"],
                        "y": data["Humidity"],
                        "type": "lines",
                        "hovertemplate": ("%{y:.0f}%<extra></extra>")
                    },
                ],
                "layout": {"title": "Average Humidity changes"}
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)