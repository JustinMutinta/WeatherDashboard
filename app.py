import pandas as pd
from dash import Dash, Input, Output, dcc, html


data = (
    pd.read_csv("weather.csv")
    .query("Location == 'Austin'")
    .assign(Date=lambda data: pd.to_datetime(data["Time"], format="%H:%M:%S"))
    .sort_values(by="Time")
)

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Temp Analytics"),
        html.P(
            children=(
                "Analyze the temp in cities over time"
            ),
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Time"],
                        "y": data["Temperature"],
                        "type": "lines",
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
                    },
                ],
                "layout": {"title": "Average Humidity changes"}
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)