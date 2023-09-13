from dash.dependencies import Output, Input, State
from dash import no_update,ctx,html
from callback_functions.main_app_class import main_app
from callback_functions.custom_helpers import create_dash_table_from_data_frame
import pandas as pd
import plotly.express as px
from connections.MySQL import get_data_as_data_frame
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash import dcc,MATCH,ALL



#this function will apply the filter values to rules repo table 
@main_app.app.callback(
    Output("rules_repo_table_container", "children",allow_duplicate=True),
    # Input("apply_filter_button_rules_repo2","n_clicks"),
    [[State(filter_id,"options"),Input(filter_id,"value")] for filter_id in main_app.environment_details['filter_ids_rule_repo'].split(',')],
    prevent_initial_call = True 
)
def apply_filter_for_rules_repo_table(*filter_options_and_values):

    if ctx.triggered_id is None : raise PreventUpdate

    filter_columns = main_app.environment_details['filter_table_columns_rules_repo'].split(',')

    filter_options = [filter_options_and_values[index][0] for index in range(0,len(filter_options_and_values))]
    
    filter_values = [filter_options_and_values[index][1] for index in range(0,len(filter_options_and_values))]

    dictionary = dict([filter_columns[index],filter_values[index]] for index in range(len(filter_values)))
    
    sql_query = f"select * from rules_repo"

    index = 0
    for column_name,filter_value in dictionary.items():
        if(filter_value is not None):
            if(len(filter_value)!=0 and len(filter_options[index]) != len(filter_value)):
                sql_query+=f" {' and ' if sql_query.find('where')!=-1 else ' where '} {column_name} in {filter_value} "
        index+=1

    sql_query = sql_query.replace("[","(").replace("]",")")

    # print(f"SQL Query =========== \n\n\n\n{sql_query}\n\n\n\n")

    data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

    if(len(data_frame != 0)):
        table = create_dash_table_from_data_frame(
            data_frame_original=data_frame,
            table_id= main_app.environment_details["rules_repo_table_id"],
            key_col_number=int(main_app.environment_details["rules_repo_table_primary_key_col_number"]),
            col_numbers_to_omit= [6],
            primary_kel_column_numbers=[int(num) for num in main_app.environment_details["rules_repo_table_primary_key_col_numbers"].split(",")],
            select_record_positon=0,
            select_record_type='radio'
            )
       
    else :
        table = "No records found for the applied filter"
    
    print("-------------------Filter Applied-----------------")
    print(sql_query)

    return table


# function for clear all button
@main_app.app.callback(
    [Output(filter_id+"_select_all","value",allow_duplicate=True) for filter_id in main_app.environment_details["filter_ids_rule_repo"].split(",")],
    Input("clear_filter_button_rules_repo","n_clicks"),
    prevent_initial_call=True
)
def clear_all_filters(n_clicks):
    return [False for filter_id in main_app.environment_details["filter_ids_rule_repo"].split(",")]



# function that will run when radio button is clicked in rules repo table.
@main_app.app.callback(
    Output({"type":f'rb_{main_app.environment_details["rules_repo_table_id"]}',"index":ALL},"value"),
    Output('home_page_contents_bottom','children'),
    Input({"type":f'{main_app.environment_details["rules_repo_table_id"]}_row_number',"index":ALL},"n_clicks"),
    State({"type":f'rb_{main_app.environment_details["rules_repo_table_id"]}',"index":ALL},"name"),
)
def radio_button_function(row_numbers,key):

    if ctx.triggered_id is None:
        raise PreventUpdate
    
    no_of_fields = 1
    rule_details = {"no_of_fields":no_of_fields}
    for dictionary in key[ctx.triggered_id["index"]] : # returns an array of dict obj's with colname:colvalu pairs
        rule_details = {**rule_details,**dictionary}
    
    main_app.rule_details = rule_details
    

    sql_query = 'show tables'

    data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

    field_mapper = []
    for i in range(no_of_fields):
        layout = html.Div(id=f'field{i+1}',children=[
            dbc.Label(f"Field{i+1} : "),
            dbc.Select(id={"type":"field_mapper","index":i+1},
                   options= [],
                   placeholder='Choose Table First...',
                   className = 'field_mapper'),
        ],
        className='label_dropdown_container')
        field_mapper.append(layout)

    layout = html.Div(children = [
        html.Div(id="rule_heading",children=[
            html.Span(id='rule_label',children=f'Selected Rule : '), 
            html.Span(id="rule_name",children=f'{rule_details["RULE_NAME"]}')
        ]),
        
        html.Div(id='rule_binding_container_inside',
                 children=[
                    html.Div(id="table_selecotr_container",children=[
                        dbc.Label(f"Select Table : "),
                        dbc.Select(id='table_selector',
                                options= [{"label" : table_name.upper(), "value":table_name} for table_name in data_frame[data_frame.columns[0]]],
                                placeholder='Select Table ...',
                                className = 'table_selector'
                            ),
                    ]),
                    
                    html.Div(id = 'field_mapper_container',children=[
                            layout for layout in field_mapper
                        ]),

                    dbc.Button("Bind",id="bind_rule"),
                    # dbc.Button("Bind & Run",id="bind_and_run_rule"),
                 ]),
        
    ],className = 'rule_binding_container')
    return [True if ctx.triggered_id["index"] == i else False for i in range(len(key))],layout
            
