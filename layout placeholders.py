from dash import Dash, html, dcc, Input, Output, ctx, callback
import pandas as pd
import geopandas as gpd
import plotly.express as px
import dash_bootstrap_components as dbc


# Import data / indexing

# Mapbox token
px.set_mapbox_access_token(open(".mapbox_token").read())

# Plotly Express figs




# Initialize Dash application
app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP]) #theme could be changed https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/



app.layout = html.Div(children=[
    dbc.Container([
        dbc.Row(html.H1(children="Risk Information per Province")), #static, but we could change via call back to "Risk Information in {Region}, put id if ever"
        
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Row(children=[
                    dbc.Stack(children=[
                        dbc.Placeholder(style={"height":50,
                                        "width":"100%"}),
                        dbc.Placeholder(style={"height":725,
                                        "width":"100%"})]
                                        ,gap=4)
                    ])
            ], width=5),

            dbc.Col(children=[
                dbc.Stack(children=[
                    dbc.Row(children=[
                        dbc.Col(children=dbc.Placeholder(style={"height":50,
                                                                "width":"100%"})),
                        dbc.Col(children=dbc.Placeholder(style={"height":50,
                                                                "width":"100%"}))
                    ]),
                    dbc.Row(children=[
                        dbc.Col(children=dbc.Placeholder(style={"height":350,
                                                                "width":"100%"})),
                        dbc.Col(children=dbc.Placeholder(style={"height":350,
                                                                "width":"100%"}))
                    ]),
                    dbc.Row(children=[
                        dbc.Col(children=
                                dbc.Placeholder(style={"height":350,
                                                    "width":"100%"}))
                    ])
                ], gap=4)
            ])
        ]),

        html.Br(),

        dbc.Row(children=[
            dbc.Col(dbc.Placeholder(style={"height":300,
                                           "width":"100%"}),
                                           width=5),
            dbc.Col(dbc.Placeholder(style={"height":300,
                                           "width":"100%"}))
        ]),

        html.Br(),

        dbc.Row(children=[
            dbc.Col(dbc.Placeholder(style={"height":300,
                                           "width":"100%"}),
                                           width=5),
            dbc.Col(dbc.Placeholder(style={"height":300,
                                           "width":"100%"}))
        ]),

        html.Br(),

        dbc.Row(
            html.H1(children="Risk Information per Region")), #static, but we could change via call back to "Risk Information in {Region}, put id if ever"


        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Placeholder(style={"height":25,
                                           "width":"100%"})],
                                           width=5)
        ]),

        html.Br(),


        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Stack(children=[
                    dbc.Placeholder(style={"height":185,
                                           "width":"100%"}),
                    dbc.Placeholder(style={"height":185,
                                           "width":"100%"})]
                ,gap=4)]
            ,width=5),
            
            dbc.Col(dbc.Placeholder(style={"height":400,
                                           "width":"100%"}))

        ])
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

