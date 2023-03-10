# RICHARD CASTRO
# TAG HISTORICAL MATRIX DASHBOARD
# DEC 2022
import pandas as pd
import dash
import copy
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, dash_table
import dash_html_components as html
import datetime as dt
from dash.dependencies import Input, Output, State, ClientsideFunction
# import dash_bootstrap_components as dbc
from dash.dependencies import State, Input, Output
from datetime import date
from controls import COUNTIES, VIRUSES, WELL_TYPES, WELL_COLORS
import numpy as np


px.set_mapbox_access_token("pk.eyJ1Ijoia2luZ2Nhc3RybzgyIiwiYSI6ImNsYnV0ejMwMjBicTgzcnBoNmFlMTA5YmwifQ.epJSJjJwbezsjKpTM8y_tA")





# SETTING UP THE FOUR INDICATORS AT TOP OF PAGE
# rt value
def rtValue():
    dff='334,805,269'
    return dff

# case rate
def caseValue():
    dff='101,719,027'
    return dff

# vaccination rate
def vaxValue():
    dff='98,772,851'
    return dff

# rt change in value
def rtChange():
    dff='1,146,833,378'
    return dff



# CONSTANTS
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

weeks = [1,2,3,4,5,6,7,8,9,10,11,12,
        13,14,15,16,17,18,19,20,21,
        22,23,24,25,26,27,28,29,30,
        31,32,33,34,35,36,37,38,39,40]





app = Dash(__name__,)
server=app.server


filter_options_virus = [
    {"label": "MonkeyPox", "value": "MP"},
    {"label": "COVID-19", "value": "CO"},
    {"label": "Influenza", "value": "IN"},
    {"label": "Common Cold", "value": "CL"}
]

filter_options_client = [
    {"label": "Kerry", "value": "Keery"},
    {"label": "PepsiCo", "value": "PepsiCo"},
    {"label": "Kelloggs", "value": "Kelloggs"}
]


# Load data
df = pd.read_csv("data/Book2.csv",low_memory=False,)

dfs = [
    {"label": str(VIRUSES[COUNTIES]), "value": str(COUNTIES)}
    for COUNTIES in VIRUSES
]

# Create app layout
app.layout = html.Div(
    [
    dcc.Store(id="aggregate_data"),
    # empty Div to trigger javascript file for graph resizing
    html.Div(id="output-clientside"),


    # TOP BAR SECTION - LOGO AND PAGE TITLE
    html.Div([
        # LOGO SECTION
        html.Div([
            html.Img(
            src=app.get_asset_url("logo.png"),
                id="tag-logo",
                style={
                    "height": "60px",
                    "width": "auto",
                    "margin-bottom": "25px",
                    },
            )],className="one-third column",),
        # TITLE SECTION
        html.Div([
            html.Div([
                html.H3(
                    "TAG Risk Matrix",
                    style={"margin-bottom": "0px"},
                    ),

                html.H5(
                    "Public Health", style={"margin-top": "0px"}
                    ),
                ])
            ],
            className="one-half column",
            id="title",
            ),
        ],
        id="header",
        className="row flex-display",
        style={"margin-bottom": "25px"},
        ),





        html.Div([
                html.Div([
                        # html.P(
                        #     "Filter by date:",
                        #     className="control_label",
                        # ),
                        #  dcc.DatePickerRange(
                        #     id='my-date-picker-range',
                        #     min_date_allowed=date(2020, 4, 1),
                        #     max_date_allowed=date(2022, 12, 15),
                        #     initial_visible_month=date(2022, 8, 5),
                        #     end_date=date(2022, 11, 25)
                        # ),

                        html.P("Select a Virus:", className="control_label"),

                        dcc.Dropdown(
                            id="virus_dropdown",
                            options=VIRUSES,
                            multi=False,
                            value=list(VIRUSES.keys()),
                            className="dcc_control",
                        ),


                        html.P("Select a State:", className="control_label"),

                        dcc.Dropdown(
                            id="state_dropdown",
                            options=COUNTIES,
                            multi=False,
                            value=list(COUNTIES.keys()),
                            className="dcc_control",
                        ),

                        # html.P("Filter by Virus:", className="control_label"),
                        #
                        # dcc.Dropdown(
                        #     id="virus_dropdown",
                        #     options=filter_options_virus,
                        #     multi=True,
                        #     value=list(VIRUSES.keys()),
                        #     className="dcc_control",
                        # ),



                        html.P("Filter by Client:", className="control_label"),

                        # dcc.Dropdown(
                        #     id="client_dropdown",
                        #     options=filter_options_client,
                        #     multi=True,
                        #     value=list(WELL_TYPES.keys()),
                        #     className="dcc_control",
                        # ),

                    ],
                    className="pretty_container three columns",
                    id="cross-filter-options",
                ),






                html.Div(
                    [
                        # 4 notification slots - need callback function for them.
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(rtValue()), html.P("Population")],
                                    id="wells",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(caseValue()), html.P("Cases")],
                                    id="gas",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(vaxValue()), html.P("Recovered")],
                                    id="oil",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(rtChange()), html.P("Tested")],
                                    id="water",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),


                        # 1ST GRAPH SECTION
                        html.Div(
                            [dcc.Graph(id="cdc_graph")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="",
        ),



        html.Div(
            [

                # 2ND GRAPH SECTION
                html.Div(
                    [dcc.Graph(id="bubble_graph")],
                    className="pretty_container seven columns",
                ),


                # 3RD GRAPH SECTION
                html.Div(
                    [dcc.Graph(id="stack_graph")],
                    className="pretty_container five columns",
                ),



            ],
            className="row flex-display",
        ),



        html.Div(
            [

                # 4TH GRAPH SECTION
                html.Div(
                    [dcc.Graph(id="")],
                    className="pretty_container seven columns",
                ),


                # 5TH GRAPH SECTION
                html.Div(
                    [dcc.Graph(id="map_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


df=pd.read_csv('data/Book6.csv')

@app.callback(
    Output("candle_graph","figure"),
    Input("virus_dropdown","value"))

def update_candle(day):
    fig = px.line(df, x="rt", y="cases", color="state")
    return fig


@app.callback(
    Output("bubble_graph","figure"),
    Input("virus_dropdown","value"))

def update_bubbles(day):
    fig = px.scatter(df, x="srt", y="rt", animation_frame="week",
               size="cr", color="state", )
    return fig




@app.callback(
    Output("stack_graph","figure"),
    Input("virus_dropdown","value"))

def update_stack(day):
    fig=px.area(df, x="week",y="cases",color="state",line_group="state")
    return fig


@app.callback(
    Output("graph", "figure"),
    Input("virus_dropdown", "value"))
def update_bar_chart(day):
    dfe = pd.read_csv('data/statert.csv')
    fig = px.bar(dfe, x = 'STATE', y = 't', title='RT')
    return fig



@app.callback(
    Output("mapgraph", "figure"),
    Input("virus_dropdown", "value"))
def update_bar_chart(day):
    mapdf = pd.read_csv('data/client_list.csv', low_memory=False)
    fig = px.scatter_mapbox(mapdf, lat="Lat", lon="Long", color="Client Name", size="Facility Type",
                      size_max=15, zoom=3)
    return fig


@app.callback(
    Output("map_graph", "figure"),
    Input("virus_dropdown", "value"))
def display_choropleth(candidate):
    df=pd.read_csv('data/lev.csv')
    fig = go.Figure(data=go.Choropleth(
    locations=df['STATENAME'], # Spatial coordinates
    z = df['ACTIVITY LEVEL'], # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    animation_frame=df['WEEK'],
    # colorbar_title = "Millions USD",
    ))

    fig.update_layout(
        # title_text = '2011 US Agriculture Exports by State',
        geo_scope='usa', # limite map scope to USA
    )

    return fig




@app.callback(
    Output("cdc_graph", "figure"),
    Input("virus_dropdown", "value"))

def update_cdc_map(day):
    df=pd.read_csv('data/stmap.csv')


    data = [dict(type='choropleth',
                 locations = df['STATENAME'].astype(str),
                 z=df['ACTIVITY LEVEL'].astype(float),
                 locationmode='USA-states')]

    # let's create some more additional, data
    for i in range(39):
        data.append(data[0].copy())
        data[-1]['z'] = data[0]['z'] * np.random.rand(*data[0]['z'].shape)

    # let's now create slider for map
    steps = []
    for i in range(len(data)):
        step = dict(method='restyle',
                    args=['visible', [False] * len(data)],
                    label='Week {}'.format(i))
        step['args'][1][i] = True
        steps.append(step)

    slider = [dict(active=0,
                    pad={"t": 1},
                    steps=steps)]
    layout = dict(geo=dict(scope='usa',
                           projection={'type': 'albers usa'}),title="CDC MAP STYLE FROM LILY'S EMAIL YESTERDAY",
                  sliders=slider)

    fig = dict(data=data,
               layout=layout)
    # plotly.offline.iplot(fig)
    return fig





# Main
if __name__ == "__main__":
    app.run_server(debug=True)
