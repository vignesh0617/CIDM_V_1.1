from dash import Output,Input,ctx, html, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from callback_functions.main_app_class import main_app
from callback_functions.custom_helpers import create_dash_table_from_data_frame,load_filter_and_table_for_rule_binding_page,load_latest_rule_binding_table
from connections.MySQL import *



@main_app.app.callback(
        Output("filters_rules_repo","children",allow_duplicate=True),
        Output("rules_repo_table_container","children",allow_duplicate=True),
        Input("refresh_button_home_page","n_clicks"),
        prevent_initial_call = 'initial_duplicate'
)
def create_filter_buttons_and_refresh_data(n_clicks):

    if (n_clicks is None  or ctx.triggered_id is None ):
        raise PreventUpdate
    
    # gets all the required inputs from the environment.txt file
    # all the values are converted to an array format and stored in corresponding variables
    
    filters,rules_repo_table = load_filter_and_table_for_rule_binding_page()

    return filters,rules_repo_table


@main_app.app.callback(
        Output("rule_binding_table_container","children",allow_duplicate=True),
        Input("refresh_button_rule_binding_page","n_clicks"),
        prevent_initial_call = 'initial_duplicate'
)
def refresh_rule_binding_table(n_clicks):

    if (n_clicks is None  or ctx.triggered_id is None ):
        raise PreventUpdate
    
    main_app.binding_id_list = []
    # gets all the required inputs from the environment.txt file
    # all the values are converted to an array format and stored in corresponding variables
    
    rule_binding_table = load_latest_rule_binding_table()

    return rule_binding_table




#The below loop is used to update the labels of each filter passed
filter_ids = main_app.environment_details['filter_ids_rule_repo'].split(',')

for i in range(len(filter_ids)):
    filter_id = filter_ids[i]

    #trying to implement a new feature
    @main_app.app.callback(
        Output(filter_id+"_drop_down","label"),
        Output(filter_id+"_select_all","value"),
        Input(filter_id,"value"),
        State(filter_id,"options"),
        # prevent_initial_call='initial_duplicate',
        # State(filter_id+"_select_all","value"),
    )
    def update_filter_label_and_options(value,options):
        
        if(len(value)==len(options)):
            return "All",True
        return str([item for item in value]).replace("[","").replace("]","").replace("'","") if len(value) !=0 else "Select...", None

    @main_app.app.callback(
        Output(filter_id+"_drop_down","label",allow_duplicate=True),
        Output(filter_id,"value",allow_duplicate=True),
        Input(filter_id+"_select_all","value"),
        State(filter_id,"options"),
        prevent_initial_call='initial_duplicate',
    )
    def update_filter_label_and_options(selected,options):
            if selected == None :
                raise PreventUpdate
            elif selected :
                return "All",[item for item in options]
            else :
                return "Select...",[]
