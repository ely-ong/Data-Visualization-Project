from dash import Dash, html, dcc, Input, Output, ctx, callback
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


# Import data / indexing
df_region_province_lookup = pd.read_excel('data101_data/region_province_lookup.xlsx')
regions = df_region_province_lookup['Region'].unique()
df_region_indexed = df_region_province_lookup.set_index('Region')

# Mapbox token
px.set_mapbox_access_token(open(".mapbox_token").read())

# Plotly Express figs




# Initialize Dash application
app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP]) #theme could be changed https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/

region_options = []
for i in regions:
    region_options.append({
        'label': i, 
        'value': i
    })

app.layout = html.Div(children=[
    dbc.Container([
        html.Br(),
        dbc.Row(html.H1(children="Risk Information per Province")), #static, but we could change via call back to "Risk Information in {Region}, put id if ever"
        
        html.Br(),

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
                        dbc.Col(children=[
                                html.H6(children="Select Region"),
                                dcc.Dropdown(
                                            region_options,
                                            region_options[0]['value'],
                                            id="region-select",
                                            clearable=False,
                                            style={"height":20,
                                                    "width":"100%"})]),
                        dbc.Col(children=[
                                html.H6(children="Select Province/District"),
                                dcc.Dropdown(
                                            id="province-select1",
                                            clearable=False,
                                            style={"height":20,
                                                     "width":"100%"})])
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
        html.Br(),

        dbc.Row(
            html.H1(children="Risk Information per Region")), #static, but we could change via call back to "Risk Information in {Region}, put id if ever"

        html.Br(),

        dbc.Row(children=[
            dbc.Col(children=[
                html.H6(children="Select Province/District to Highlight"),
                dcc.Dropdown(
                            id="province-select2",
                            clearable=False,
                            style={"height":30,
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
            
        ]),

        html.Br(),
        html.Br()

    ])
])

# function to reuse for updating the options of a single province dropdown
def update_province_options(output_id, input_id):

    @callback(
        Output(output_id, "options"),
        Output(output_id, "value"),
        Input(input_id, "value")
    )
    def update_options(selected_region):
        df_provinces = df_region_indexed.loc[selected_region]

        province_options = [{'label': i, 'value': i} for i in df_provinces.Province.unique()]
        value = province_options[0]['value']

        return province_options, value 

# set province options for first dropdown
update_province_options("province-select1", "region-select")

# set province options for second dropdown
update_province_options("province-select2", "region-select")


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)