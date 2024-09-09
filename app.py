from dash import Dash, dcc, html, Input, Output, no_update
import pandas as pd
import dash_design_kit as ddk
import plotly.express as px
import json

app = Dash(__name__)
server = app.server  # expose server variable for Procfile


app.layout = ddk.App([
    dcc.Interval(id='interval', n_intervals=1, max_intervals=1),
    ddk.Header([
        ddk.Logo(src=app.get_asset_url('logo.png')),
        ddk.Title('Dash Enterprise Sample Application'),
    ]),
    ddk.Row(children=[
        ddk.Card(width=20, children=[
            html.Div(id='display')
        ]),
        ddk.Card(width=80, children=[
            ddk.Graph(id='update-graph', style={'height':650}),
        ]),
    ]),

])


@app.callback(Output('update-graph', 'figure'),
              [Input('interval', 'interval')],)
def update_graph(value):
    url = 'https://data.pmel.noaa.gov/pmel/erddap/tabledap/argo_eng_navis.csv?floatid%2Ctime%2Clongitude%2Clatitude&time<=now-11days'
    print(url)
    df = pd.read_csv(url, skiprows=[1])
    df = df.groupby(by=['floatid'], as_index=False).last()
    figure = px.scatter_mapbox(df, lat='latitude', lon='longitude', color='floatid', custom_data='floatid')
    return figure


@app.callback(
    [
        Output('display', 'children')
    ],
    [
        Input('update-graph', 'clickData')
    ], prevent_initial_call=True
)
def show_click(in_click):
    if in_click is not None:
        s = json.dumps(in_click, indent=4)
        return [s]
    else:
        no_update


if __name__ == '__main__':
    app.run_server(debug=True)
