from dash import dcc, html
import dash_bootstrap_components as dbc
from components.navbar import navbar
from connections.MySQL import get_data_as_data_frame
from callback_functions.main_app_class import main_app
from callback_functions.custom_helpers import create_dash_table_from_data_frame,load_latest_rule_binding_table

rule_binding_table = load_latest_rule_binding_table()

layout = html.Div(id = "rule_binding_page_main_container",children=[
    navbar,
    html.Div(id="rule_binding_page_heading",
             children=[
             html.Span("Select a rule and start execution"),
             ]),
    html.Div(id="rule_binding_table_container",
            children=[
            rule_binding_table
            ]),
    html.Div(id="rule_binding_button_container",
            children=[
            dbc.Button("Run",id="run_binded_rule"),
        #     dbc.Button("Delete",id="delete_binded_rule"),
            ]),
    dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Confirmation"), close_button=True),
                dbc.ModalBody("Delete Selected Rules?"),
                dbc.ModalFooter(children = [
                    dbc.Button("Yes",id="proceed_delete"),
                    dbc.Button("No",id="cancel_delete"),
                ]
                ),
            ],
            id="confirm_dialog_box",
            centered=True,
            is_open=False,
        ),
    html.Span(id="refresh_button_rule_binding_page", className="bi bi-arrow-clockwise refresh_button_position btn-white circle btn-animated"),
    
],className="main-container")