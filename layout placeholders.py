from dash import Dash, html, dcc, Input, Output, ctx, callback
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


# Import data / indexing
df_region_province_lookup = pd.read_excel(
    'data101_data/region_province_lookup.xlsx')
regions = df_region_province_lookup['Region'].unique()
df_region_indexed = df_region_province_lookup.set_index('Region')

df_roof_and_wall_categories = pd.read_excel(
    'data101_data/roof_and_wall_cleaned.xlsx')
df_roof_wall_indexed = df_roof_and_wall_categories.set_index(
    ['Region', 'Province'])

df_water_sources = pd.read_excel(
    'data101_data/water_sources_cleaned.xlsx', index_col=0)
df_water_sources_indexed = df_water_sources.set_index(['Region', 'Province'])

df_toilet_sources = pd.read_excel(
    'data101_data/toilet_types_cleaned.xlsx', index_col=0)
df_toilet_sources_indexed = df_toilet_sources.set_index(['Region', 'Province'])

df_elem = pd.read_excel('data101_data/elem_students_cleaned.xlsx', index_col=0)
df_elem_indexed = df_elem.set_index(['Region', 'Province'])

df_secondary = pd.read_excel(
    'data101_data/secondary_students_cleaned.xlsx', index_col=0)
df_secondary_indexed = df_secondary.set_index(['Region', 'Province'])

df_pop_by_gender_age = pd.read_csv('data101_data/bidirectional_df.csv')

average_gdf = gpd.read_file(
    'data101_data/final_aggregate.geojson', driver='GeoJSON')
average_gdf_indexed = average_gdf.set_index('adm2_name')

cyclone_gdf = gpd.read_file(
    'data101_data/final_cyclone.geojson', driver='GeoJSON')
cyclone_gdf_indexed = cyclone_gdf.set_index('adm2_name')

flood_gdf = gpd.read_file('data101_data/final_flood.geojson', driver='GeoJSON')
flood_gdf_indexed = flood_gdf.set_index('adm2_name')

landslide_gdf = gpd.read_file(
    'data101_data/final_landslide.geojson', driver='GeoJSON')
landslide_gdf_indexed = landslide_gdf.set_index('adm2_name')

pop = pd.read_excel('data101_data/pop_per_reg.xlsx')

response = pd.read_excel('data101_data/response_per_reg.xlsx')

evac_and_schools_df = pd.read_excel('data101_data/evac_and_schools_df_cleaned.xlsx', sheet_name='consolidated')

vuln_df = pd.read_excel('data101_data/vulnerable_groups_cleaned.xlsx', sheet_name='consolidated')

health_faci_df = pd.read_excel('data101_data/health_facilities_cleaned.xlsx', sheet_name='consolidated')

# Mapbox token
px.set_mapbox_access_token(open(".mapbox_token").read())


# Initialize Dash application
app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP])  # theme could be changed https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/

region_options = []
for i in regions:
    region_options.append({
        'label': i,
        'value': i
    })

app.layout = html.Div(children=[
    dbc.Container([
        html.Br(),
        # static, but we could change via call back to "Risk Information in {Region}, put id if ever"
        dbc.Row(html.H1(children="Risk Information per Province")),

        html.Br(),

        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Row(children=[
                    dbc.Stack(children=[
                        dbc.Col(children=[  # radio buttons, filters for choropleth
                            html.H6(children="Select Risk Class Type"),
                            dbc.RadioItems(options=['Average', 'Typhoon', 'Flood', 'Landslide'],
                                           value='average',
                                           id='choropleth-select',
                                           inline=True,
                                           className='mb-2',
                                           style={"height": 20,
                                                  "width": "100%"})]),
                        dcc.Loading(id="map-loading",
                                    type="circle",
                                    children=[html.H5(id="choropleth-title"),
                                              dcc.Graph(id="ph-map")]
                                    # style={"height": 725, "width": "100%"} # choropleth map
                                    )], gap=1)
                ])
            ], width=5),

            dbc.Col(children=[
                dbc.Stack(children=[
                    dbc.Row(children=[
                        dbc.Col(children=[  # region dropdown
                                html.H6(children="Select Region"),
                                dcc.Dropdown(
                                    region_options,
                                    region_options[0]['value'],
                                    id="region-select",
                                    clearable=False,
                                    style={"height": 20,
                                           "width": "100%"})]),
                        dbc.Col(children=[  # province dropdown
                                html.H6(children="Select Province/District"),
                                dcc.Dropdown(
                                    id="province-select1",
                                    clearable=False,
                                    style={"height": 20,
                                           "width": "100%"})]),
                    ]),

                    dbc.Row(children=[
                        dbc.Col(children=[  # bidirectional population and age
                            html.H6(id="pop-bidirectional-title"),
                            dcc.Graph(
                                id="pop-bidirectional",
                                style={"height": 350,
                                       "width": "100%"})]),
                        dbc.Col(children=[ 
                            html.Br(),
                            dbc.Row( # vulnerable groups single values
                                dbc.CardGroup([
                                    dbc.Card(
                                        [dbc.CardImg(src="/static/images/disabled_male.png", 
                                                     top=True,
                                                     title="Disabled Males"),
                                         dbc.CardBody(children=[
                                             html.H6(id='disabled_male',
                                                     style={'text-align': 'center'}
                                                     ),
                                             html.H6("Disabled Males", 
                                                     style={'font-size': '12px',
                                                            'text-align': 'center'})])],
                                        outline=True, color="light"),
                                    dbc.Card(
                                        [dbc.CardImg(src="/static/images/elderly_male.png", 
                                                     top=True,
                                                     title="Elderly Males"),
                                         dbc.CardBody(children=[
                                             html.H6(id='older_male',
                                                     style={'text-align': 'center'}),
                                                     
                                             html.H6("Elderly Males", 
                                                    style={'font-size': '12px',
                                                           'text-align': 'center'})])],
                                        outline=True, color="light"),
                                    dbc.Card(
                                        [dbc.CardImg(src="/static/images/children-headed_male.png", 
                                                     top=True,
                                                     title="Male Child-headed Families"),
                                         dbc.CardBody(children=[
                                             html.H6(id='child_headed_male', 
                                                     style={'text-align': 'center'}
                                                     ),
                                                     
                                             html.H6("Male Child-headed Families", 
                                                    style={'font-size': '12px',
                                                           'text-align': 'center'})])],
                                        outline=True, color="light"),
                                    dbc.Card(
                                        [dbc.CardImg(src="/static/images/solo_parent_male.png", 
                                                     top=True,
                                                     title="Male Single Parents"),
                                         dbc.CardBody(children=[
                                             html.H6(id='solo_parent_male',
                                                     style={'text-align': 'center'}
                                                     ),
                                                     
                                             html.H6("Male Single Parents", 
                                                    style={'font-size': '12px',
                                                           'text-align': 'center'})])],
                                        outline=True, color="light")
                                ])),
                            html.Br(),
                            dbc.Row(
                                dbc.CardGroup([
                                    dbc.Card(
                                        [dbc.CardImg(src="/static/images/disabled_female.png", 
                                                     top=True,
                                                     title="Disabled Females"),
                                         dbc.CardBody(children=[
                                             html.H6(id='disabled_female', 
                                                     style={'text-align': 'center'}
                                                     ),
                                                     
                                             html.H6("Disabled Females", 
                                                    style={'font-size': '12px',
                                                        'text-align': 'center'})])],
                                        outline=True, color="light"),
                                    dbc.Card(
                                        [dbc.CardImg(src="/static/images/elderly_female.png", 
                                                     top=True,
                                                     title="Elderly Females"),
                                         dbc.CardBody(children=[
                                             html.H6(id='older_female',
                                                     style={'text-align': 'center'}
                                                     ),
                                                     
                                             html.H6("Elderly Females", 
                                                    style={'font-size': '12px',
                                                           'text-align': 'center'})])],
                                        outline=True, color="light"),
                                    dbc.Card(
                                        [dbc.CardImg(src="/static/images/children-headed_female.png", 
                                                     top=True,
                                                     title="Female Child-headed Families"),
                                         dbc.CardBody(children=[
                                             html.H6(id='child_headed_female',
                                                     style={'text-align': 'center'}
                                                     ),
                                                     
                                             html.H6("Female Child-headed Families", 
                                                    style={'font-size': '12px',
                                                           'text-align': 'center'})])],
                                        outline=True, color="light"),
                                    dbc.Card(
                                        [dbc.CardImg(src="/static/images/solo_parent_female.png", 
                                                     top=True,
                                                     title="Female Single Parents"),
                                         dbc.CardBody(children=[
                                             html.H6(id='solo_parent_female',
                                                     style={'text-align': 'center'}
                                                     ),
                                                     
                                             html.H6("Female Single Parents", 
                                                    style={'font-size': '12px',
                                                           'text-align': 'center'})])],
                                        outline=True, color="light")
                                ])
                            )
                        ])
                    ]),

                    dbc.Row(children=[
                        dbc.Col(dbc.Card(  # num of evac centers single value
                            [dbc.CardImg(src="/static/images/evac_center.png", 
                                         top=True,
                                         title="Evacuation Centers"),
                             dbc.CardBody(children=[
                                html.H3(id='evac-center-values', 
                                        style={'text-align': 'center'}),
                                html.H5("Evacuation Centers", 
                                        style={'text-align': 'center'})
                            ])],
                            outline=True, color="light"),
                            style={"height": 350,
                                   "width": "100%"}),

                        dbc.Col(dbc.Card(  # num of schools single value
                            [dbc.CardImg(src="/static/images/school.png", 
                                         top=True,
                                         title="Schools"),
                             dbc.CardBody(children=[
                                html.H3(id='school-values',
                                        style={'text-align': 'center'}),
                                html.H5("Schools",
                                        style={'text-align': 'center'})
                            ])],
                            outline=True, color="light"),
                            style={"height": 350,
                                   "width": "100%"}),

                        dbc.Col(children=[  # elem pie
                                html.H6(id="elem-title"),
                                dcc.Graph(
                                    id="elem-pie",
                                    style={"height": 350,
                                           "width": "100%"})]),
                        dbc.Col(children=[  # secondary students pie
                                html.H6(id="secondary-title"),
                                dcc.Graph(
                                    id="secondary-pie",
                                    style={"height": 350,
                                           "width": "100%"})])
                    ])
                ], gap=4)
            ])
        ]),

        html.Br(),

        dbc.Row(children=[ #health facilities available
            dbc.Col(children=[
                dbc.Row(
                    dbc.CardGroup([
                        dbc.Card(
                            [dbc.CardImg(src="/static/images/brgy_health_station.png", 
                                         top=True,
                                         title="Barangay Health Stations"),
                             dbc.CardBody(children=[
                                 html.H4(id='brgy-health-station-values',
                                         style={'text-align': 'center'}
                                         ),
                                                     
                                 html.H6("Barangay Health Stations", 
                                          style={
                                          'text-align': 'center'})])],
                            outline=True, color="light"),
                        dbc.Card(
                            [dbc.CardImg(src="/static/images/hospital.png", 
                                         top=True,
                                         title="Hospitals"),
                             dbc.CardBody(children=[
                                 html.H4(id='hospital-values',
                                         style={'text-align': 'center'}
                                         ),
                                                     
                                 html.H6("Hospitals", 
                                          style={
                                          'text-align': 'center'})])],
                            outline=True, color="light"),
                        dbc.Card(
                            [dbc.CardImg(src="/static/images/health_clinic_laboratory.png", 
                                         top=True,
                                         title="General Clinic Laboratories"),
                             dbc.CardBody(children=[
                                 html.H4(id='gen-clinic-laboratory-values',
                                         style={'text-align': 'center'}
                                         ),
                                                     
                                 html.H6("General Clinic Laboratories", 
                                          style={
                                          'text-align': 'center'})])],
                            outline=True, color="light")
                    ])
                ),
                dbc.Row(
                    dbc.CardGroup([
                        dbc.Card(
                            [dbc.CardImg(src="/static/images/rural.png", 
                                         top=True,
                                         title="Rural Health Units"),
                             dbc.CardBody(children=[
                                 html.H4(id='rural-health-unit-values',
                                         style={'text-align': 'center'}
                                         ),
                                                     
                                 html.H6("Rural Health Units", 
                                          style={
                                          'text-align': 'center'})])],
                            outline=True, color="light"),
                        dbc.Card(
                            [dbc.CardImg(src="/static/images/infirmary.png", 
                                         top=True,
                                         title="Infirmaries"),
                             dbc.CardBody(children=[
                                 html.H4(id='infirmary-values',
                                         style={'text-align': 'center'}
                                         ),
                                                     
                                 html.H6("Infirmaries", 
                                          style={
                                          'text-align': 'center'})])],
                            outline=True, color="light"),
                        dbc.Card(
                            [dbc.CardImg(src="/static/images/birthing_home.png", 
                                         top=True,
                                         title="Birthing Homes"),
                             dbc.CardBody(children=[
                                 html.H4(id='birth-homes-values',
                                         style={'text-align': 'center'}
                                         ),
                                                     
                                 html.H6("Birthing Homes", 
                                          style={
                                          'text-align': 'center'})])],
                            outline=True, color="light")
                    ]))],
            width=5),
            dbc.Col(dbc.Placeholder(style={"height": 300,  # health personnel bar
                                           "width": "100%"}))
        ]),

        html.Br(),

        dbc.Row(children=[
            dbc.Col(children=[  # wall-roof heatmap
                    html.H5(id="heatmap-title"),
                    dcc.Graph(
                        id="heatmap",
                        style={"height": 500,
                               "width": "100%"})],
                    width=5),
            dbc.Col(children=[  # water sources availability pie
                    html.H5(id="water-title"),
                    dcc.Graph(
                        id="water-pie",
                        style={"height": 500,
                               "width": "100%"})]),
            dbc.Col(children=[  # toilet facility availability pie
                    html.H5(id="toilet-title"),
                    dcc.Graph(
                        id="toilet-pie",
                        style={"height": 500,
                               "width": "100%"})])
        ]),

        html.Br(),
        html.Br(),

        dbc.Row(
            html.H1(children="Risk Information per Region")),  # static, but we could change via call back to "Risk Information in {Region}, put id if ever"

        html.Br(),

        dbc.Row(children=[
            dbc.Col(children=[
                # province/district dropwdown
                html.H6(children="Select Province/District to Highlight"),
                dcc.Dropdown(
                    id="province-select2",
                    value="province-select1",
                    clearable=False,
                    style={"height": 30,
                           "width": "100%"})],
                    width=5)
        ]),

        html.Br(),


        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Stack(children=[
                    dbc.Col(children=[  # pop per province bar
                        html.H6(id="pop-per-prov-title"),
                        dcc.Graph(
                            id="pop-per-prov",
                            style={"height": 300,
                                   "width": "100%"})]),
                    dbc.Col(children=[  # response facilities per province bar
                        html.H6(id="response-per-prov-title"),
                        dcc.Graph(
                            id="response-per-prov",
                            style={"height": 300,
                                   "width": "100%"})
                    ])
                ])
            ], width=5),

            dbc.Col(dbc.Placeholder(style={"height": 400,  # health personnel to population scatter
                                           "width": "100%"}))

        ]),

        html.Br(),
        html.Br()

    ])
])

# set province options and value for first dropdown


@callback(
    Output("province-select1", "options"),
    Output("province-select1", "value"),
    Output("province-select2", "options"),
    Input("region-select", "value")
)
def update_province_options(selected_region):
    df_provinces = df_region_indexed.loc[selected_region]

    province_options = [{'label': i, 'value': i}
                        for i in df_provinces.Province.unique()]
    value = province_options[0]['value']

    return province_options, value, province_options

# set province value for second dropdown


@callback(
    Output("province-select2", "value"),
    Input("province-select1", "value")
)
def update_province_select2(selected_province):

    return selected_province


# set up placeholder for unavailable data
fig_none = go.Figure()
fig_none.add_trace(go.Scatter(
    x=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
    y=[0, 4, 5, 1, 2, 3, 2, 4, 2, 1],
    mode="text",
    text=["", "", "", "", "", "Data unavailable", "", "", ""],
    textfont_size=24,
))

fig_none.update_layout(
    xaxis={'visible': False},
    yaxis={'visible': False})


@callback(
    Output("pop-bidirectional-title", "children"),
    Input("province-select1", "value")
)
def set_pop_bidirectional_title(selected_province):
    return f'Population of {selected_province} by Age Group and Sex'


@callback(
    Output("pop-bidirectional", "figure"),
    Input("province-select1", "value")
)
def update_pop_bidirectional(selected_province):
    def sort_by_age_grp(df):
        grp_dct_map = {'0 - 4': 0, '5 - 9': 1, '10 - 14': 2, '15 - 19': 3, '20 - 24': 4,  # dictionary for ordering age groups
                       '25 - 29': 5, '30 - 34': 6, '35 - 39': 7, '40 - 44': 8, '45 - 49': 9,
                       '50 - 54': 10, '55 - 59': 11, '60 - 64': 12, '65 - 69': 13, '70 - 74': 14,
                       '75 - 79': 15, '>= 80': 16}

        df['age_index'] = df['Age_Group'].map(
            grp_dct_map)  # create new column of index
        # sort df by index starting from youngest to oldest
        df = df.set_index('age_index').sort_index()

        return df

    grpby_ph = df_pop_by_gender_age[df_pop_by_gender_age['Province'] == selected_province].groupby(
        by='Age_Group', as_index=False, sort=False).sum()
    grpby_ph = sort_by_age_grp(grpby_ph)

    df = grpby_ph

    fig_bidirectional_pop = go.Figure()

    # Create the bidirectional graph
    fig_bidirectional_pop.add_trace(go.Bar(
        x=-df['Male'].values,
        y=df['Age_Group'],
        name='Male',
        text=df['Male'].values,
        hoverinfo='name+text',
        orientation='h',
        marker_color='#01365c'
    )
    )

    fig_bidirectional_pop.add_trace(go.Bar(
        x=df['Female'].values,
        y=df['Age_Group'],
        name='Female',
        text=df['Female'].values,
        hoverinfo='name+text',
        orientation='h',
        marker_color='#ffb5b5')
        # .data[0]
    )

    # Set layout for the graph
    fig_bidirectional_pop.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        xaxis=dict(
            title="Population",
            tickvals=[-260000, -240000, -220000, -200000, -180000, -160000, -140000, -120000, -100000, -80000, -60000, -40000, -20000, 0,
                      20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000, 180000, 200000, 220000, 240000, 260000],
            ticktext=['260k', '240k', '220k', '200k', '180k', '160k', '140k', '120k', '100k', '80k', '60k', '40k', '20k', '0',
                      '20k', '40k', '60k', '80k', '100k', '120k', '140k', '160k', '180k', '200k', '220k', '240k', '260k']
        ),
        yaxis_title="Age Group",
        yaxis_autorange='reversed',
        showlegend=True,
        barmode='relative',
        bargap=0.05,
        bargroupgap=0
    )

    return fig_bidirectional_pop

# SINGLE VALUES VULNERABLE GROUPS CALLBACKS

@callback(
    Output("disabled_male", "children"),
    Input("province-select1", "value")
)
def set_disabled_m_values(selected_province):
    disabled_m = vuln_df.query(f"province=='{selected_province}'")["disability_male"]
    return "{:,}".format(disabled_m.iloc[0]) 

@callback(
    Output("older_male", "children"),
    Input("province-select1", "value")
)
def set_old_m_values(selected_province):
    old_male =  vuln_df.query(f"province=='{selected_province}'")["older_male"]
    return "{:,}".format(old_male.iloc[0]) 

@callback(
    Output("child_headed_male", "children"),
    Input("province-select1", "value")
)
def set_childhead_m_values(selected_province):
    child_headed_m = vuln_df.query(f"province=='{selected_province}'")["child_headed_male"]
    return "{:,}".format(child_headed_m.iloc[0]) 

@callback(
    Output("solo_parent_male", "children"),
    Input("province-select1", "value")
)
def set_solo_parent_m_values(selected_province):
    solo_par_m = vuln_df.query(f"province=='{selected_province}'")["solo_parent_male"]
    return "{:,}".format(solo_par_m.iloc[0]) 

@callback(
    Output("disabled_female", "children"),
    Input("province-select1", "value")
)
def set_disabled_f_values(selected_province):
    disabled_f = vuln_df.query(f"province=='{selected_province}'")["disability_female"]
    return "{:,}".format(disabled_f.iloc[0]) 

@callback(
    Output("older_female", "children"),
    Input("province-select1", "value")
)
def set_old_f_values(selected_province):
    old_female =  vuln_df.query(f"province=='{selected_province}'")["older_female"]
    return "{:,}".format(old_female.iloc[0]) 

@callback(
    Output("child_headed_female", "children"),
    Input("province-select1", "value")
)
def set_childhead_f_values(selected_province):
    child_headed_f = vuln_df.query(f"province=='{selected_province}'")["child_headed_female"]
    return "{:,}".format(child_headed_f.iloc[0]) 

@callback(
    Output("solo_parent_female", "children"),
    Input("province-select1", "value")
)
def set_solo_parent_f_values(selected_province):
    solo_par_f = vuln_df.query(f"province=='{selected_province}'")["solo_parent_female"]
    return "{:,}".format(solo_par_f.iloc[0])

# SINGLE VALUES EVAC-SCHOOL CALLBACKS
@callback(
    Output("evac-center-values", "children"),
    Input("province-select1", "value")
)
def set_evac_center_values(selected_province):
    evac_center_value = evac_and_schools_df.query(f"province=='{selected_province}'")["evacuation_centers"]
    return "{:,}".format(evac_center_value.iloc[0]) 


@callback(
    Output("school-values", "children"),
    Input("province-select1", "value")
)
def set_school_values(selected_province):
    school_value = evac_and_schools_df.query(f"province=='{selected_province}'")["total_schools"]
    return "{:,}".format(school_value.iloc[0]) 

# SINGLE VALUES HEALTH FACILITIES CALLBACKS
@callback(
    Output("brgy-health-station-values", "children"),
    Input("province-select1", "value")
)
def set_brgy_health_station_values(selected_province):
    brgy_health_station = health_faci_df.query(f"province=='{selected_province}'")["brgy_health_station"]
    return "{:,}".format(brgy_health_station.iloc[0])

@callback(
    Output("hospital-values", "children"),
    Input("province-select1", "value")
)
def set_hospital_values(selected_province):
    hosp =  health_faci_df.query(f"province=='{selected_province}'")["hospital"]
    return "{:,}".format(hosp.iloc[0]) 

@callback(
    Output("gen-clinic-laboratory-values", "children"),
    Input("province-select1", "value")
)
def set_gen_clinic_laboratory_values(selected_province):
    gen_clinic = health_faci_df.query(f"province=='{selected_province}'")["gen_clinic_laboratory"]
    return "{:,}".format(gen_clinic.iloc[0]) 

@callback(
    Output("rural-health-unit-values", "children"),
    Input("province-select1", "value")
)
def set_rural_health_unit_values(selected_province):
    rural_unit = health_faci_df.query(f"province=='{selected_province}'")["rural_health_unit"]
    return "{:,}".format(rural_unit.iloc[0]) 

@callback(
    Output("infirmary-values", "children"),
    Input("province-select1", "value")
)
def set_infirmary_values(selected_province):
    infirmary =  health_faci_df.query(f"province=='{selected_province}'")["infirmary"]
    return "{:,}".format(infirmary.iloc[0]) 

@callback(
    Output("birth-homes-values", "children"),
    Input("province-select1", "value")
)
def set_birthing_homes_values(selected_province):
    birth_home = health_faci_df.query(f"province=='{selected_province}'")["birthing_homes"]
    return "{:,}".format(birth_home.iloc[0]) 


@callback(
    Output("elem-title", "children"),
    Input("province-select1", "value")
)
def set_elem_title(selected_province):
    return 'Percentage of Elementary Students in '+selected_province+' by Sex'


@callback(
    Output("secondary-title", "children"),
    Input("province-select1", "value")
)
def set_secondary_title(selected_province):
    return 'Percentage of Secondary Students in '+selected_province+' by Sex'


@callback(
    Output("pop-per-prov-title", "children"),
    Input("region-select", "value")
)
def set_pop_per_prov_title(selected_region):
    return 'Population per Province in '+selected_region


@callback(
    Output("response-per-prov-title", "children"),
    Input("region-select", "value")
)
def set_pop_per_prov_title(selected_region):
    return 'Total Response Facilities per Province in '+selected_region


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
    elem_students_counts = df_elem_indexed.loc[selected_region,
                                               selected_province]

    # if data row is full of 0, set figure to none
    if (elem_students_counts == 0).all():
        fig_elem = fig_none

    # converting dataframe row of counts to array of toilet type counts to assign to plotly go.figure values
    elem_students_counts = elem_students_counts.values.flatten()

    # creating color map
    sex_color_map = {'Male': '#01365c', 'Female': '#ffb5b5'}

    # converting color map to pd.Series to assign to go.figure colors value
    sex_color_map = pd.Series(sex_color_map)

    fig_elem = go.Figure(data=[go.Pie(labels=sex,
                                      values=elem_students_counts)])

    # setting title and colors
    fig_elem.update_layout(
        autosize=True,
        showlegend=False,
        margin={'b': 0, 'l': 0, 't': 0, 'r': 0})
    fig_elem.update_traces(textinfo='label+percent',
                           hoverinfo='label+value',
                           marker=dict(colors=sex_color_map))

    # selecting dataframe row from selected region and province
    secondary_students_counts = df_secondary_indexed.loc[selected_region,
                                                         selected_province]

    # if data row is full of 0, set figure to none
    if (secondary_students_counts == 0).all():
        fig_secondary = fig_none

    # converting dataframe row of counts to array of toilet type counts to assign to plotly go.figure values
    secondary_students_counts = secondary_students_counts.values.flatten()

    fig_secondary = go.Figure(data=[go.Pie(labels=sex,
                                           values=secondary_students_counts)])

    # setting title and colors
    fig_secondary.update_layout(
        autosize=True,
        showlegend=False,
        margin={'b': 0, 'l': 0, 't': 0, 'r': 0})
    fig_secondary.update_traces(textinfo='label+percent',
                                hoverinfo='label+value',
                                marker=dict(colors=sex_color_map))

    return fig_elem, fig_secondary


@callback(
    Output("heatmap-title", "children"),
    Input("province-select1", "value")
)
def set_heatmap_title(selected_province):
    return "Percentage of Shelters by Wall and Roof Categories in "+selected_province


@callback(
    Output("water-title", "children"),
    Input("province-select1", "value")
)
def set_water_title(selected_province):
    return "Percentage of Water Sources by Category in "+selected_province


@callback(
    Output("toilet-title", "children"),
    Input("province-select1", "value")
)
def set_toilet_title(selected_province):
    return "Percentage of Toilet Facility Types in "+selected_province


@callback(
    Output("heatmap", "figure"),
    Input("region-select", "value"),
    Input("province-select1", "value")
)
def update_heatmap(selected_region, selected_province):

    # selecting dataframe row from selected region and province
    shelter_counts = df_roof_wall_indexed.loc[selected_region,
                                              selected_province]

    # if data row is full of 0, set figure to none
    if (shelter_counts == 0).all():

        fig_shelter = fig_none

        return fig_shelter

    # converting dataframe row of counts to array of shelter type percentages to fill up new dataframe
    shelter_counts = shelter_counts.values.flatten()
    counts_sum = sum(shelter_counts)
    shelter_percentages = [(round(i/counts_sum*100, 2))
                           for i in shelter_counts]

    # creating modified dataframe of selected counts for heatmap
    wall_categories = ['Strong Wall', 'Light Wall', 'Salvaged Wall']
    roof_categories = ['Strong Roof', 'Light Roof', 'Salvaged Roof']
    df_shelters = pd.DataFrame(index=wall_categories)

    # filling up dataframe with array of shelter counts
    df_shelters[roof_categories[0]] = shelter_percentages[0:3]
    df_shelters[roof_categories[1]] = shelter_percentages[3:6]
    df_shelters[roof_categories[2]] = shelter_percentages[6:9]

    fig_shelter = px.imshow(df_shelters,
                            text_auto=True,
                            color_continuous_scale='turbid',
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

    # selecting dataframe row from selected region and province
    water_source_categories_counts = df_water_sources_indexed.loc[
        selected_region, selected_province]

    # if data row is full of 0, set figure to none
    if (water_source_categories_counts == 0).all():
        fig_water = fig_none

    else:

        # converting dataframe row of counts to array of water source categories to assign to plotly go.figure values
        water_source_categories_counts = water_source_categories_counts.values.flatten()

        # creating color map
        water_color_map = {'Faucet/Community System': '#72e5ef',
                           'Tubed/Piped': '#214d4e',
                           'Dug well': '#239eb3',
                           'Bottled Water': '#bfd6fa',
                           'Natural Sources': '#0f5eb0',
                           'Peddler/Others/Not reported': '#aeabab'}

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
            margin={'l': 0, 't': 3, 'r': 0})
        fig_water.update_traces(
            hoverinfo='label+value',
            marker=dict(colors=water_color_map))

    # creating array of toilet types to assign to plotly go.figure labels
    toilet_types = df_toilet_sources_indexed.columns

    # selecting dataframe row from selected region and province
    toilet_type_counts = df_toilet_sources_indexed.loc[selected_region,
                                                       selected_province]

    # if data row is full of 0, set figure to none
    if (toilet_type_counts == 0).all():
        fig_toilet = fig_none

    else:
        # converting dataframe row of counts to array of toilet type counts to assign to plotly go.figure values
        toilet_type_counts = toilet_type_counts.values.flatten()

        # creating color map
        toilet_color_map = {'Water Sealed': '#72e5ef',
                            'Closed Pit': '#115d52',
                            'Open Pit': '#0ba47e',
                            'None': '#aeabab'}

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
            margin={'l': 0, 't': 3, 'r': 0})
        fig_toilet.update_traces(
            hoverinfo='label+value', marker=dict(colors=toilet_color_map))

    return fig_water, fig_toilet


@callback(
    Output("choropleth-title", "children"),
    Input("choropleth-select", "value")
)
def choropleth_title(selected_type):
    if 'average' == selected_type:
        return "Average Risk Class per Province"

    elif 'typhoon' == selected_type:
        return "Typhoon Risk Class (above Category 3) per Province"

    elif 'flood' == selected_type:
        return "Flood Risk Class per Province"

    else:
        return "Landslide Risk Class per Province"


@callback(
    Output('ph-map', 'figure'),
    Input('choropleth-select', 'value'),
)
def display_map(selected_type):
    if 'average' == selected_type:
        geodf = average_gdf_indexed

        map_fig = px.choropleth_mapbox(geodf,
                                       geojson=geodf.geometry,
                                       locations=geodf.index,
                                       color='AvgRisk_Class',
                                       color_continuous_scale=px.colors.sequential.OrRd,
                                       range_color=(0, 4),
                                       mapbox_style="carto-positron",
                                       title="Average Risk Class per Province",
                                       hover_name=geodf.index,
                                       hover_data=[
                                           'AvgRisk_Class', 'AvgRisk_Text'],
                                       center={'lat': 12.099568,
                                               'lon': 122.733168},
                                       height=725,
                                       zoom=4.5)
        map_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    elif 'typhoon' == selected_type:
        geodf = cyclone_gdf_indexed

        map_fig = px.choropleth_mapbox(geodf,
                                       geojson=geodf.geometry,
                                       locations=geodf.index,
                                       color='Cy_Class',
                                       color_continuous_scale=px.colors.sequential.Burg,
                                       range_color=(0, 4),
                                       mapbox_style="carto-positron",
                                       title="Typhoon Risk Class (above Category 3) per Province",
                                       hover_name=geodf.index,
                                       hover_data=['Cy_Freq',
                                                   'Cy_Class', 'Cy_Text'],
                                       center={'lat': 12.099568,
                                               'lon': 122.733168},
                                       height=725,
                                       zoom=4.5)
        map_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    elif 'flood' == selected_type:
        geodf = flood_gdf_indexed

        map_fig = px.choropleth_mapbox(geodf,
                                       geojson=geodf.geometry,
                                       locations=geodf.index,
                                       color='FloodClass',
                                       color_continuous_scale=px.colors.sequential.Teal,
                                       range_color=(0, 4),
                                       mapbox_style="carto-positron",
                                       title="Flood Risk Class per Province",
                                       hover_name=geodf.index,
                                       hover_data=['AvgFLRisk',
                                                   'FloodClass', 'FloodText'],
                                       center={'lat': 12.099568,
                                               'lon': 122.733168},
                                       height=725,
                                       zoom=4.5)
        map_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    else:
        geodf = landslide_gdf_indexed

        map_fig = px.choropleth_mapbox(geodf,
                                       geojson=geodf.geometry,
                                       locations=geodf.index,
                                       color='LS_Class',
                                       color_continuous_scale=px.colors.sequential.Brwnyl,
                                       range_color=(0, 4),
                                       mapbox_style="carto-positron",
                                       title="Landslide Risk Class per Province",
                                       hover_name=geodf.index,
                                       hover_data=['LS_Risk',
                                                   'LS_Class', 'LS_Text'],
                                       center={'lat': 12.099568,
                                               'lon': 122.733168},
                                       height=725,
                                       zoom=4.5)
        map_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return map_fig


@callback(
    Output('pop-per-prov', 'figure'),
    Input('region-select', 'value'),
    Input('province-select2', 'value'),
)
def pop_per_prov(selected_region, selected_province):
    region_name = selected_region

    # Filter the DataFrame by the given region
    region_data = pop[pop['Region'] == region_name].copy().reset_index()

    # Add a 'province_id' column to the filtered DataFrame
    region_data['province_id'] = [str(i) for i in region_data.index]

    color_discrete_sequence = ['lightslategray',]*len(region_data)
    index = region_data.loc[region_data['Province']
                            == selected_province].index[0]
    color_discrete_sequence[index] = ['crimson']  # index

    fig_pop = px.bar(region_data, x='Province', y='Total Population',
                     color='province_id',
                     color_discrete_sequence=color_discrete_sequence,
                     )

    return fig_pop


@callback(
    Output('response-per-prov', 'figure'),
    Input('region-select', 'value'),
    Input('province-select2', 'value'),
)
def response_per_prov(selected_region, selected_province):
    region_name = selected_region

    # Filter the DataFrame by the given region
    region_data = response[response['Region']
                           == region_name].copy().reset_index()

    # Add a 'province_id' column to the filtered DataFrame
    region_data['province_id'] = [str(i) for i in region_data.index]

    pattern_shape_sequence = ['',]*len(region_data)
    index = region_data.loc[region_data['Province']
                            == selected_province].index[0]
    pattern_shape_sequence[index] = ['x', 'x', 'x']  # index

    fig_resp = px.bar(region_data, x="Province", y=["T_Evacuation", "T_Health", "T_School"],
                      # title="Total Response Facilities",
                      pattern_shape="province_id", pattern_shape_sequence=pattern_shape_sequence)

    return fig_resp


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
