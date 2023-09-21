from components.navbar import get_navbar
from dash import dcc, html
from components.side_filter_tab import layout as side_filter_tab
from callback_functions.main_app_class import main_app
from components.score_card import layout as score_card



layout = html.Div(children=[
    get_navbar(main_app.environment_details['score_card_link']),
    side_filter_tab,
    score_card,
    dcc.Download("data_to_download")
],className="main-container flex-container")