from dash import html, dcc, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from remotely.remotelyconfigmanager.config_handler import Database
from remotely.remotely_app.components.component_util import create_table
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import UnmappedInstanceError

session = Database("sqlite:///config.db")

config_table = create_table("ALL-hosts")

layout = html.Div(
    [
        dbc.Container(
            [
                html.Br(),
                html.Div(id="dummy", style={"display": "none"}),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                config_table,
                                html.Div(id='selected-row')
                            ], className='col-md-6 border-right'
                        ),
                        dbc.Col(
                            [
                                        dbc.Form(
                                            [
                                                dbc.Label("Hostname"),
                                                dbc.Input(
                                                    type="text", id="hostname-input"
                                                ),
                                            ]
                                        ),
                                        dbc.Form(
                                            [
                                                dbc.Label("Switch Root"),
                                                dbc.Input(
                                                    type="text", id="switch-root-input"
                                                ),
                                            ]
                                        ),
                                        html.Br(),
                                        dbc.Button(
                                            "Submit",
                                            color="primary",
                                            id="submit-button",
                                            n_clicks=0,
                                        ),
                            ]
                        ),
                    ]
                ),
            ]
        ),
    ]
)


@callback(
    Output("ALL-hosts", "data"),
    Output("ALL-hosts", "columns"),
    Input("ALL-hosts", "data_timestamp"),
    Input("dummy", "children"),
)
def update_config_table(timestamp, dummy):
    try:
        configs = session.get_hosts()
        columns = [{"name": col, "id": col} for col in configs.columns]
        data = configs.to_dict("records")
        return data, columns
    except (OperationalError, UnmappedInstanceError):
        session.rollback()
        return [], []

@callback(
    Output('selected-row', 'children'),
    [Input('ALL-hosts', 'selected_rows')]
)
def update_output(selected_rows):
    if selected_rows:
        return f"You have selected row {selected_rows}"
    else:
        return ""


@callback(
    Output("submit-button", "n_clicks"),
    Input("submit-button", "n_clicks"),
    State("hostname-input", "value"),
    State("switch-root-input", "value"),
)
def insert_host(n_clicks, hostname, switch_root):
    if n_clicks > 0:
        # Create a new Host object
        host = session.create_hosts(hostname, switch_root)
        # Reset the input values
        hostname = None
        switch_root = None
        return 0

    return n_clicks
