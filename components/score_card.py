from dash import html,dcc
from callback_functions.score_card_functions import *

layout = html.Div([
    html.Div([
            html.Div(id = "filters_rule_binding",className="side-filter-tab-contents"),
            html.Button("Clear", id = "clear_filter_button", className="btn-theme1"),
            # html.Button("Apply", id = "apply_filter_button", className="btn-theme1")
        ],className="filter-header",id = "filter_header"),

    html.Div([
                dcc.Graph(id="pie_chart1"),
                dcc.Graph(id="pie_chart2"),
                html.Div(id="score_card_rules_table",className="top-table")
        
    ],id="score_card_contents_top",className="score-card-page-contents-top"),
    
    html.Div([
        dcc.Graph(id="trend_chart"),
        html.Div(id="score_card_binded_rules",className = "bottom-table"),
    ],id="score_card_contents_bottom",className="score-card-page-contents-bottom"),

    html.Span(id="refresh_button_score_card_page", className="bi bi-arrow-clockwise refresh_button_position btn-white circle btn-animated"),
    
],id = "score_card_failed_records_container")