from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from remotely.remotely_app.components.configuration_generator import (
    layout as conf_layout,
)
from remotely.remotely_app.components.mainpage import layout as main_layout
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container
from remotely.remotelyconfigmanager.config_handler import Database

session = Database("sqlite:///config.db")

session.create_tables()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/style.css'])

tabs = dbc.Tabs(
    [
        dbc.Tab(main_layout, label="MAIN-PAGE"),
        dbc.Tab(conf_layout, label="CONFIGURATION GENERATOR"),
    ]
)

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button("Search", color="primary", className="ms-2", n_clicks=0),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("REMOTELY", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
)

app.layout = html.Div([navbar, tabs])


@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
