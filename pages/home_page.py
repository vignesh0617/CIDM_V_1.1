import dash_bootstrap_components as dbc
from components.navbar import navbar
from dash import  html,dcc
from connections.MySQL import get_connection
from callback_functions.main_app_class import main_app
from callback_functions.custom_helpers import *
from callback_functions.home_page_functions import *
from callback_functions.load_function import *
from components.home_page_contents_top import layout as home_page_contents_top



layout = html.Div(children=[
    navbar,
    html.Div(id='home_page_contents_top',
             children = home_page_contents_top),
    html.Div(id='home_page_contents_bottom',
             children = " Please select a rule to Bind"), 
    html.Span(id="refresh_button_home_page", className="bi bi-arrow-clockwise refresh_button_position btn-white circle btn-animated"),                                     
],className="main-container")