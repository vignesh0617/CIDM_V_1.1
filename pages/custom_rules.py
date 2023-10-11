from dash import html
import dash_bootstrap_components as dbc
from components.navbar import get_navbar
from callback_functions.main_app_class import main_app
from callback_functions.custom_rules_functions import *

requesting_user = dbc.Row(
    [
        dbc.Label("Requesting User", width=2),
        dbc.Col([
            dbc.Input(type="text", id="requesting_user",placeholder="User Name"),
            dbc.FormFeedback(type="valid"),
            dbc.FormFeedback("Enter a valid user",type="invalid")],
            width=10,
        ),
    ],
    className="mb-3",
)

user_email = dbc.Row(
    [
        dbc.Label("User Email",width=2),
        dbc.Col([
            dbc.Input(type="email",id="user_email",placeholder="Email Id"),
            dbc.FormFeedback(type="valid"),
            dbc.FormFeedback("Enter a valid email",type="invalid")],
            width=10,
        ),
    ],
    className="mb-3",
)

reuquest_type = dbc.Row(
    [
        dbc.Label("Request_type",width=2),
        dbc.Col([
            dbc.RadioItems(options=[
                {'label':'Business Desc','value':'business'},
                {'label':'SQL','value':'sql'}
            ],id="request_type",value="business"),
            dbc.FormFeedback(type="valid"),
            dbc.FormFeedback("Select a request type",type="invalid")],
            width=10,
        ),
    ],
    className="mb-3",
)


business_desc_sql = dbc.Row(
    [
        dbc.Label("Business Desc/SQL",width=2),
        dbc.Col([
            dbc.Textarea(id="business_desc_sql",placeholder="Business Desc / SQL",className="mb-3"),
            dbc.FormFeedback(type="valid"),
            dbc.FormFeedback("Enter Business desc/SQL",type="invalid")],
            width=10,
        ),
    ],
    className="mb-3",
)


status = dbc.Row(
    [
        dbc.Label("Status",width=2),
        dbc.Col([
            dbc.Input(type="text",id="status",placeholder="Status"),
            dbc.FormFeedback(type="valid"),
            dbc.FormFeedback("Enter Status",type="invalid")],
            width=10,
        ),
    ],
    className="mb-3",
)


submit = html.Div(
    dbc.Button("Submit",id="cudf_submit_btn",className="btn-theme1"),
    className="cudf_sb",
)

layout = html.Div(children=[
    html.Div(className="app_bg"),
    get_navbar(active_link=main_app.environment_details['custom_user_defined_rules']),
    dbc.Form([
        requesting_user,
        user_email,
        reuquest_type,
        business_desc_sql,
        status,
        submit
    ])
],id="custom_rules_container", className="main-container")