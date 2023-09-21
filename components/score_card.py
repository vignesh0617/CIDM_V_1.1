from dash import html,dcc
from callback_functions.score_card_functions import *

layout = html.Div([
    html.Div([
            # html.Div([
                dcc.Graph(id="pie_chart1"),
                dcc.Graph(id="pie_chart2"),
                html.Div(id="score_card_rules_table",className="top-table")
        # ],className="top-figures",id="top_figures"), 
        
    ],id="score_card_contents_top",className="score-card-page-contents-top"),
    html.Div([
        dcc.Graph(id="trend_chart"),
        html.Div(id="score_card_binded_rules",className = "bottom-table"),
        html.Div(id="score_card_failed_records",className="bottom-table-failed-records")
    ],id="score_card_contents_bottom",className="score-card-page-contents-bottom"),

    html.Span(id="refresh_button_score_card_page", className="bi bi-arrow-clockwise refresh_button_position btn-white circle btn-animated"),
    
],id = "score_card_failed_records_container")