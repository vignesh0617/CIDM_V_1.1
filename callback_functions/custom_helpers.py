
import jwt
import dash_bootstrap_components as dbc
from dash import html, Dash
from connections.MySQL import get_data_as_data_frame
from callback_functions.main_app_class import main_app
import pandas as pd

def load_filter_and_table_for_rule_binding_page():

    filter_tables = main_app.environment_details['filter_table_names_rules_repo'].split(',')
    filter_tables_columns = main_app.environment_details['filter_table_columns_rules_repo'].split(',')
    filter_tables_labels = main_app.environment_details['filter_table_labels_rules_repo'].split(',')
    filter_ids = main_app.environment_details['filter_ids_rule_repo'].split(',')

    filters = []

    for i in range(len(filter_tables)):
        table_name = filter_tables[i]
        column_name = filter_tables_columns[i]
        column_label = filter_tables_labels[i]
        filter_id = filter_ids[i]

        sql_1 = f"select distinct {column_name} from {table_name}"
        data_frame = get_data_as_data_frame(sql_query=sql_1  , cursor= main_app.cursor)
        # this is the new layout model for the filter buttons with select all check box features
        layout = html.Div([
                    dbc.Label(column_label,className = "filter-label"),
                    dbc.DropdownMenu([
                        dbc.Checkbox(id=filter_id+"_select_all",label="Select All"),
                        dbc.Checklist(id=filter_id,
                                      options=data_frame[data_frame.columns[0]],
                                      value=[])
                    ],
                    label = "Select...",
                    id=filter_id+"_drop_down",
                    className= "filter_drop_down"
                    )
                ],className = "filter-card",
                  id = f"filter_card_{i}",
                )
        
        filters.append(layout)

    
    sql_query = f"select * from rules_repo"

    data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

    table = create_dash_table_from_data_frame(
            data_frame_original=data_frame,
            table_id= main_app.environment_details["rules_repo_table_id"],
            key_col_number=int(main_app.environment_details["rules_repo_table_primary_key_col_number"]),
            col_numbers_to_omit= [6],
            primary_kel_column_numbers=[int(num) for num in main_app.environment_details["rules_repo_table_primary_key_col_numbers"].split(",")],
            select_record_positon=0,
            select_record_type='radio'
            )
    
    return filters,table
    


def load_latest_rule_binding_table():
    sql_query = "select * from rule_binding"
    data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

       
    rule_binding_table = create_dash_table_from_data_frame(
        data_frame_original=data_frame,
        table_id= main_app.environment_details["rule_binding_table_id"],
        key_col_number= int(main_app.environment_details["rule_binding_table_primary_key_col_number"]),
        primary_kel_column_numbers= [int(x) for x in main_app.environment_details["rule_binding_table_primary_key_col_numbers"].split(",")],
        col_numbers_to_omit=[int(x) for x in main_app.environment_details["rule_binding_table_col_numbers_to_omit"].split(",")],
        select_record_positon=1+len(data_frame.columns)-len(main_app.environment_details["rule_binding_table_col_numbers_to_omit"].split(",")),
        select_record_type="checkbox",
    )

    return rule_binding_table
    

#for creating JWT
def create_token(payload, 
                secret_key = main_app.environment_details['secret_key'], 
                algorithm = main_app.environment_details['algorithm']):
    return jwt.encode(payload, secret_key, algorithm)

#for decoding JWT
def decode_token(token, 
                secret_key = main_app.environment_details['secret_key'], 
                algorithm = main_app.environment_details['algorithm']):
    return jwt.decode(token, secret_key, algorithm)
    
# For creating a dash table from a dataframe
# data_frame_original ---> table will be created based on this dataframe
# table_id ---> this table id should be unique for identifying a table
# key_col_number ----> 0th index. each row will store this correspoding data_frame_original.iloc[<row>,key_column_number] in its "key" attribute. This can be used later if required
# action_col_number --->0th index. a link kind of style will be applied to col_number mentioned here. Define a corresponding function to get executed when this data is pressed
# primary_key_col_numbers ----> 1st index . index's mentioned here, will get saved in form of dicitonary [{"col name1" : "vale1" },{"col name2" : "vale2" }......{{"col namen" : "valen" }}]
# capital_headings ----> Headings of the table header will be Capital letters if this value is True else it will be Title
# col_numbers_to_omit ---->0th index. these index's will be omitted while creating tables in front end  
# select_record_type ------> indicates if to select the single(radio button) or multiple(check box) records . Options to pass "single" or "multiple"
# select_record_positon ---> 0th index. where to insert the selected record
def create_dash_table_from_data_frame(
        data_frame_original:pd.DataFrame,
        table_id:str,
        key_col_number:int,
        action_col_numbers:list[int] = [],
        primary_kel_column_numbers:list[int] = [],
        capital_headings:bool =False,
        col_numbers_to_omit:list[int] = [],
        select_record_type:str = "radio",
        select_record_positon:int = None,
        generate_srno:bool = True,
        disable_check_box:bool = True,
    ):

    print( f"\n\n\n------------ select_record_positon = {select_record_positon} ---------")
    # creates a duplicate data_frame which will omit the col_number mentioned in  "col_numbers_to_omit"
    if col_numbers_to_omit: # this if block will execute only if col_numbers_to_omit array is not empty
        col_range = []
        for i in range(data_frame_original.shape[1]):
            if(i not in col_numbers_to_omit):
                col_range.append(i)
        
        data_frame = data_frame_original.iloc[:,col_range]
    else :
        data_frame = data_frame_original

    
    table_headings = [] # stores all th html values
    table_records = [] # stores all td html vales
    no_of_rows = len(data_frame.index) 
    no_of_cols = len(data_frame.columns)

    for col_label in data_frame.columns:
    
        table_headings.append(
            html.Th(
                children = col_label.upper() if capital_headings else col_label.title()
            )
        )

    if generate_srno:
        table_headings.insert(0,
            html.Th(
                children = "S.NO" if capital_headings else "S.no"
            )
        )

    if select_record_positon is not None :#and (select_record_positon == index ):
        if select_record_type.lower() == 'radio':
            table_headings.insert(select_record_positon,
                html.Th(
                    children = "SELECT" if capital_headings else "Select"
                )
            )
        else : #select_record_type.lower() == 'checkbox' :
            # cb = dbc.Checkbox(id=f"cb_all_{table_id}",label=""),
            table_headings.insert(select_record_positon,
                html.Th(
                    children = [
                        # "Select all",
                        dbc.Checkbox(id=f"cb_all_{table_id}",label="SELECT ALL" if capital_headings else "Select All")
                    ]
                )
            )
    
    unique_id = 0 # this unique_id is used to identify each key attribute in "td" 
    for row in range(no_of_rows):
        records = []
        for col in range(no_of_cols):
            records.append(
                html.Td(
                    children = data_frame.iloc[row,col],
                    id = {'type' : f"{table_id}_row_data",'index' : unique_id} if col in action_col_numbers else {"type":f"{table_id}_row{row}" ,"index" : col},#f"{table_id}_row_data_row-{row}_col-{col}" ,
                    key = {"column_name" : data_frame_original.columns[col],"column_data" : data_frame_original.iloc[row,col] , "primary_keys" : [{data_frame_original.columns[index-1] : data_frame_original.iloc[row,index-1] } for index in primary_kel_column_numbers ]} if col in action_col_numbers else {"column_name" : data_frame_original.columns[col],"column_data" : data_frame_original.iloc[row,col] },
                    className = "table_action" if col in action_col_numbers and data_frame.iloc[row,col]!=0 else ""
                )
            )

                       
            if col in action_col_numbers:
                unique_id+=1
        if generate_srno :
            records.insert(0,
                html.Td(
                    children = row+1,
                    )
            )
        if select_record_positon is not None:#  and select_record_positon == col:
                if select_record_type.lower() == 'radio':
                    records.insert(select_record_positon,
                        html.Td(
                            children = [
                                dbc.RadioButton(id={"type":f"rb_{table_id}","index":row},
                                                label="",
                                                name=[{data_frame_original.columns[index-1] : data_frame_original.iloc[row,index-1] } for index in primary_kel_column_numbers ],
                                                value=False)#=data_frame.iloc[row,key_col_number])
                            ],
                            
                        )
                    )
                else :
                    records.insert(select_record_positon,
                        html.Td(
                            children = [
                                dbc.Checkbox(id={"type":f"cb_{table_id}","index":row},
                                             label="",
                                             name=[{data_frame_original.columns[index-1] : data_frame_original.iloc[row,index-1] } for index in primary_kel_column_numbers ],
                                             disabled=disable_check_box,
                                             value=False)#=data_frame.iloc[row,key_col_number])
                            ],
                            
                        )
                    )
        table_records.append(
            html.Tr(
                children = records,
                id = {
                    'type' : f"{table_id}_row_number",
                    'index' : row
                },
                # id = f"{table_id}_row{row}",
                key = data_frame.iloc[row,key_col_number]
            )
        )
    
    if no_of_rows == 0:
        table_records.append(
            html.Tr(
                children = [
                    html.Td(
                        children="No Records to display",
                        colSpan= len(table_headings)
                    )
                ]
            )
        )
    final_table = html.Table([
        html.Thead(
            html.Tr(
                table_headings
            )
        ),
        html.Tbody(
            table_records
        )
    ],id = table_id ,className="table table-hover table-light")


    return final_table



