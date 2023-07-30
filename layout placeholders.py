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

df_roof_and_wall_categories = pd.read_excel('data101_data/roof_and_wall_cleaned.xlsx')
df_roof_wall_indexed = df_roof_and_wall_categories.set_index(['Region', 'Province'])

df_water_sources = pd.read_excel('data101_data/water_sources_cleaned.xlsx', index_col=0)
df_water_sources_indexed = df_water_sources.set_index(['Region', 'Province'])

df_toilet_sources = pd.read_excel('data101_data/toilet_types_cleaned.xlsx', index_col=0)
df_toilet_sources_indexed = df_toilet_sources.set_index(['Region', 'Province'])

df_elem = pd.read_excel('data101_data/elem_students_cleaned.xlsx', index_col=0)
df_elem_indexed = df_elem.set_index(['Region', 'Province'])

df_secondary = pd.read_excel('data101_data/secondary_students_cleaned.xlsx', index_col=0)
df_secondary_indexed = df_secondary.set_index(['Region', 'Province'])

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
                                                     "width":"100%"})]),
                    ]),
                    
                    dbc.Row(children=[
                        dbc.Col(children=dbc.Placeholder(style={"height":350,
                                                                "width":"100%"})),
                        dbc.Col(children=dbc.Placeholder(style={"height":350,
                                                                "width":"100%"}))
                    ]),
                    dbc.Row(children=[
                        dbc.Col(children=dbc.Placeholder(style={"height":350,
                                                                "width":"100%"})),
                        dbc.Col(children=dbc.Placeholder(style={"height":350,
                                                                "width":"100%"})),
                        dbc.Col(children=[
                                html.H5(id="elem-title"),
                                dcc.Graph(
                                        id="elem-pie",
                                        style={"height":350,
                                        "width":"100%"})]),
                        dbc.Col(children=[
                                html.H5(id="secondary-title"),
                                dcc.Graph(
                                        id="secondary-pie",
                                        style={"height":350,
                                                "width":"100%"})])                                       
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
            dbc.Col(children=[
                    html.H5(id="heatmap-title"),
                    dcc.Graph(
                        id="heatmap",
                        style={"height":500,
                                           "width":"100%"})],
                                           width=5),
            dbc.Col(children=[
                    html.H5(id="water-title"),
                    dcc.Graph(
                        id="water-pie",
                        style={"height":500,
                                "width":"100%"})]),
            dbc.Col(children=[
                    html.H5(id="toilet-title"),
                    dcc.Graph(
                        id="toilet-pie",
                        style={"height":500,
                                "width":"100%"})])
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

@callback(
    Output("elem-title", "children"),
    Input("province-select1", "value")
)
def set_elem_title(selected_province):
    return 'Percentage of Elementary Students in '+selected_province.title()+' by Sex'

@callback(
    Output("secondary-title", "children"),
    Input("province-select1", "value")
)
def set_secondary_title(selected_province):
    return 'Percentage of Secondary Students in '+selected_province.title()+' by Sex'

@callback(
    Output("elem-pie", "figure"),
    Output("secondary-pie", "figure"),
    Input("region-select", "value"),
    Input("province-select1", "value")
)
def update_students_pie_graphs(selected_region, selected_province):

    # creating array of sex types to assign to plotly go.figure labels
    sex = ['Male',
        'Female']

    # selecting dataframe row from selected region and province
    elem_students_counts = df_elem_indexed.loc[selected_region, selected_province]

    # converting dataframe row of counts to array of toilet type counts to assign to plotly go.figure values
    elem_students_counts = elem_students_counts.values.flatten()

    # creating color map
    sex_color_map = {'Male':'#01365c','Female':'#ffb5b5'}

    # converting color map to pd.Series to assign to go.figure colors value
    sex_color_map = pd.Series(sex_color_map)

    fig_elem = go.Figure(data=[go.Pie(labels=sex,
                                values=elem_students_counts)])
    
    # setting title and colors
    fig_elem.update_layout(
                            autosize=True,
                            showlegend=False,
                            margin={'b':0, 'l':0, 't':0, 'r':0})
    fig_elem.update_traces(textinfo='label+percent',
                            hoverinfo='label+value', 
                           marker=dict(colors=sex_color_map))

    # selecting dataframe row from selected region and province
    secondary_students_counts = df_secondary_indexed.loc[selected_region, selected_province]

    # converting dataframe row of counts to array of toilet type counts to assign to plotly go.figure values
    secondary_students_counts = secondary_students_counts.values.flatten()

    fig_secondary = go.Figure(data=[go.Pie(labels=sex,
                                values=secondary_students_counts)])
    
    # setting title and colors
    fig_secondary.update_layout(
                                autosize=True, 
                                showlegend=False,
                                margin={'b':0, 'l':0, 't':0, 'r':0})
    fig_secondary.update_traces(textinfo='label+percent', 
                                hoverinfo='label+value', 
                                marker=dict(colors=sex_color_map))

    return fig_elem, fig_secondary


@callback(
    Output("heatmap-title", "children"),
    Input("province-select1", "value")
)
def set_heatmap_title(selected_province):
    return "Percentage of Shelters by Wall and Roof Categories in "+selected_province.title()

@callback(
    Output("water-title", "children"),
    Input("province-select1", "value")
)
def set_water_title(selected_province):
    return "Percentage of Water Sources by Category in "+selected_province.title()

@callback(
    Output("toilet-title", "children"),
    Input("province-select1", "value")
)
def set_toilet_title(selected_province):
    return "Percentage of Toilet Facility Types in "+selected_province.title()


@callback(
    Output("heatmap", "figure"),
    Input("region-select", "value"),
    Input("province-select1", "value")
)
def update_heatmap(selected_region, selected_province):

    # selecting dataframe row from selected region and province
    shelter_counts = df_roof_wall_indexed.loc[selected_region, selected_province]

    # converting dataframe row of counts to array of shelter type percentages to fill up new dataframe
    shelter_counts = shelter_counts.values.flatten()
    counts_sum = sum(shelter_counts)
    shelter_percentages = [(round(i/counts_sum*100,2)) for i in shelter_counts]

    # creating modified dataframe of selected counts for heatmap
    wall_categories = ['Strong Wall', 'Light Wall', 'Salvaged Wall']
    roof_categories = ['Strong Roof', 'Light Roof', 'Salvaged Roof']
    df_shelters = pd.DataFrame(index = wall_categories)

    # filling up dataframe with array of shelter counts
    df_shelters[roof_categories[0]] = shelter_percentages[0:3]
    df_shelters[roof_categories[1]] = shelter_percentages[3:6]
    df_shelters[roof_categories[2]] = shelter_percentages[6:9]

    fig_shelter = px.imshow(df_shelters, 
                        text_auto=True, 
                        color_continuous_scale = 'turbid',
                        labels=dict(x='Roof Category',
                                    y='Wall Category',
                            color='Percentage'))

    fig_shelter.update_xaxes(side="top")

    fig_shelter.update_layout(
                            width=500,
                            height=500)

    return fig_shelter

@callback(
    Output("water-pie", "figure"),
    Output("toilet-pie", "figure"),
    Input("region-select", "value"),
    Input("province-select1", "value")
)
def update_water_toilet_pie_graphs(selected_region, selected_province):

    water_source_categories = df_water_sources_indexed.columns

    #selecting dataframe row from selected region and province
    water_source_categories_counts = df_water_sources_indexed.loc[selected_region, selected_province]

    # converting dataframe row of counts to array of water source categories to assign to plotly go.figure values
    water_source_categories_counts = water_source_categories_counts.values.flatten()

    # creating color map
    water_color_map = {'Faucet/Community System':'#72e5ef', 
                        'Tubed/Piped':'#214d4e', 
                        'Dug well':'#239eb3', 
                        'Bottled Water':'#bfd6fa', 
                        'Natural Sources':'#0f5eb0', 
                        'Peddler/Others/Not reported':'#aeabab'}

    # converting color map to pd.Series to assign to go.figure colors value
    water_color_map = pd.Series(water_color_map)

    fig_water = go.Figure(data=[go.Pie(labels=water_source_categories,
                             values=water_source_categories_counts)])

    # setting colors
    fig_water.update_layout(
                            autosize=True,
                            legend=dict(
                            orientation="h",
                            font=dict(size=8)),
                            margin={'l':0, 't':3, 'r':0})
    fig_water.update_traces(
                            hoverinfo='label+value', 
                            marker=dict(colors=water_color_map))
    

    # creating array of toilet types to assign to plotly go.figure labels
    toilet_types = df_toilet_sources_indexed.columns

    # selecting dataframe row from selected region and province
    toilet_type_counts = df_toilet_sources_indexed.loc[selected_region, selected_province]

    # converting dataframe row of counts to array of toilet type counts to assign to plotly go.figure values
    toilet_type_counts = toilet_type_counts.values.flatten()

    # creating color map
    toilet_color_map = {'Water Sealed':'#72e5ef', 
                        'Closed Pit':'#115d52', 
                        'Open Pit':'#0ba47e', 
                        'None':'#aeabab'}

    # converting color map to pd.Series to assign to go.figure colors value
    toilet_color_map = pd.Series(toilet_color_map)

    fig_toilet = go.Figure(data=[go.Pie(labels=toilet_types,
                                values=toilet_type_counts)])

    # setting colors
    fig_toilet.update_layout(
                            autosize=True,
                            legend=dict(
                                orientation="h",
                                font=dict(size=8)),
                            margin={'l':0, 't':3, 'r':0})
    fig_toilet.update_traces(hoverinfo='label+value', marker=dict(colors=toilet_color_map))

    return fig_water, fig_toilet


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)