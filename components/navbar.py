import dash_bootstrap_components as dbc
from callback_functions.custom_helpers import main_app
from dash import html,dcc,ctx,MATCH,ALL
from dash.dependencies import Output , Input, State
from callback_functions.custom_helpers import decode_token
import time

navbar = html.Div([
    html.Nav([
        html.Ul([
            
            dcc.Link("CIDM",id='logo',href=main_app.environment_details['home_page_link']),
            dcc.Link("Rule Binding",id={"type" : "nav_link","index":0},href=main_app.environment_details['home_page_link']),
            dcc.Link("Rule Execution",id={"type" : "nav_link","index":1},href=main_app.environment_details['rule_execution_link']),
            # dcc.Link("CIDM",id="home_page_link",href=main_app.environment_details['home_page_link']),
            # dcc.Link("Rule Binding",id="rule_execution_link",href=main_app.environment_details['home_page_link']),
            # dcc.Link("Rule Execution",id="rule_execution_link",href=main_app.environment_details['rule_execution_link']),
            # dcc.Link("Logout",id="logout_link",href=main_app.environment_details['logout_page_link'])
        ])
    ],className="navbar")
],className="navbar-container")


# @main_app.app.callback(
#     Output("home_page_link","className"),
#     Output("logout_link","style"),
#     Input ("url2","pathname"),
#     State("token","data")
# )
# def highlight_active_link_and_toggle_logout_link(pathname,token):
#     try:
#         payload = decode_token(token)
#         session_not_over = payload['session_end_time'] > int(time.time())
#         if session_not_over:
#             if pathname == main_app.environment_details['home_page_link'] :
#                 return "active-link",{}
#             elif pathname == main_app.environment_details['login_page_link'] or pathname == main_app.environment_details['logout_page_link']:
#                 return "",{"display" : "none"}
#             else :
#                 return "",{}
#         return "",{"display" : "none"}
#     except Exception as e :
#         return "",{"display" : "none"}



@main_app.app.callback(
    Output({"type" : "nav_link","index":ALL},"className"),
    Input ("url2","pathname"),
    # Input({"type" : "nav_link","index":ALL},"n_clicks"),
)
def highlight_active_link(pathname):
    arr = [main_app.environment_details['home_page_link'],main_app.environment_details['rule_execution_link']]
    index = arr.index(pathname)
    className = ["" for i in range(len(arr))]
    className[index]='active-link'
    return className