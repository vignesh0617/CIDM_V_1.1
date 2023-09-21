from dash import html, Input, Output , State,ALL,ctx, MATCH,no_update
from dash.exceptions import PreventUpdate
from callback_functions.main_app_class import main_app
from connections.MySQL import get_data_as_data_frame


@main_app.app.callback(
    Output({"type":"field_mapper","index":ALL},"options"),
    Output({"type":"field_mapper","index":ALL},"value"),
    Input("table_selector","value"),
)
def update_column_values_in_rule_binding(table_name):

    if table_name is None:
        return [[] for i in range(main_app.rule_details["no_of_fields"])],["" for i in range(main_app.rule_details["no_of_fields"])]

    sql_query = f"show columns from {table_name}"
    data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

    options = [{"label" : column_name, "value" : column_name} for column_name in data_frame[data_frame.columns[0]]]
    return [ options for i in range(main_app.rule_details["no_of_fields"])],[ options[0]["value"] for i in range(main_app.rule_details["no_of_fields"])]

@main_app.app.callback(
    Output("info_toast","children"),
    Output("info_toast","header"),
    Output("info_toast","icon"),
    Output("info_toast","duration"),
    Output("info_toast","is_open"),
    Input("bind_rule","n_clicks"),
    State("table_selector","value"),
    State({"type":"field_mapper","index":ALL},"value"),
    prevent_initial_call = True,
)
def bind_rules(n_clicks,table_name,fields):
    if n_clicks is None :
        raise PreventUpdate
    
    try:
        if table_name is None or None in fields:
            msg = 'Please select Table and Field name before binding'
            header = 'Warning'
            icon = "warning"
        else :
            
            args = (
                    main_app.rule_details["RULE_ID"],
                    table_name,
                    fields[0],
                    main_app.rule_details["RULE_TYPE"],
                    main_app.rule_details["RULE_NAME"],
                    0 # if this is set to 1 then Stored procedure will bind and run the rule. Else it will bind alone
                )
            proc_name = 'bind_one_field_rule'
            main_app.cursor.callproc(proc_name,args=args)
            final_result  = None
            latest_result = None
            for stored_result in main_app.cursor.stored_results():
                latest_result= stored_result.fetchall()
            
            for result in latest_result:
                final_result = result

            if final_result[0] == 200:
                header = "Success!!"
                icon = "success"
            elif final_result[0] == 409:
                header = "Warning"
                icon = "warning"
            elif final_result[0] == 500:
                header = "Internal Error"
                icon = "warning"
            msg = final_result[1]
    except Exception as e:
        print(f"--------------{e} -------------")
        msg = "Error in SQL Execution.Please contact Support"
        header = 'danger'
        icon = "Error!!"
    duration = 3500
    return msg,header,icon,duration,True

##############
# @main_app.app.callback(
#     Output({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"value"),
#     Input({"type":f"{main_app.environment_details['rule_binding_table_id']}_row_number","index":ALL},"value"),
#     State({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"name"),
#     State({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"value")
# )
# def test(rows,name,values):
    
#     if ctx.triggered_id is None:
#         raise PreventUpdate
#     index = ctx.triggered_id['index']
#     binding_id = name[index]
#     flag = values[index]#ctx.triggered[0]["value"]
#     if(flag) and binding_id not in main_app.binding_id_list:
#         main_app.binding_id_list.append(binding_id)#insert(len(fl),binding_id)
#     else:
#         main_app.binding_id_list.remove(binding_id)

#     print(f"\n\n\n----\n1)ctx.triggered_id =  {ctx.triggered_id} \n2)index = {index}\n3)flag = {values}")
#     return values
###########################
###########################
# @main_app.app.callback(
#     Output({"type":"rule_binding_page_headeing","index":ALL},"children"),
#     Input({"type":"rule_binding_table_row_number","index":ALL},"n_clicks"),
#     # State({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"name"),
#     # State({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"value")
# )
# def test(rows):#,name,values):
    
#     print ("++++++++++triggered+++++++++++++++=")
#     return f"changed_{rows}"

###############################

@main_app.app.callback(
    Output("rule_binding_page_heading","children"),
    Output({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"value"),
    Output(f"cb_all_{main_app.environment_details['rule_binding_table_id']}","value"),
    Input({"type":f"{main_app.environment_details['rule_binding_table_id']}_row_number","index":ALL},"n_clicks"),
    State({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"value"),
    State({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"name"), 
)
def check_box_function_for_selecting_rules_to_run(n_clicks,checkbox_flag,name):
      

    if ctx.triggered_id is None or n_clicks.count(None) == len(n_clicks):
        raise PreventUpdate
    
    index = ctx.triggered_id['index']
    binding_id = name[index][0]["RULE_BINDING_ID"]

    if binding_id not in main_app.binding_id_list:
        main_app.binding_id_list.append(binding_id)
    else:
        main_app.binding_id_list.remove(binding_id)

    checkbox_flag[index] = not checkbox_flag[index]
    flag = checkbox_flag.count(True)==len(checkbox_flag)
    return f"hey there - {main_app.binding_id_list}",checkbox_flag , True if flag else None  #no_update if checkbox_flag.count(True)!=len(checkbox_flag) else True# f"changed--{main_app.binding_id_list} - {n_clicks} - {n_clicks_2}", 


@main_app.app.callback(
    Output("info_toast","children",allow_duplicate=True),
    Output("info_toast","header",allow_duplicate=True),
    Output("info_toast","icon",allow_duplicate=True),
    Output("info_toast","duration",allow_duplicate=True),
    Output("info_toast","is_open",allow_duplicate=True),
    Output({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"value",allow_duplicate=True),
    Output(f"cb_all_{main_app.environment_details['rule_binding_table_id']}","value",allow_duplicate=True),
    Output("refresh_button_rule_binding_page","n_clicks",allow_duplicate=True),
    Output("confirm_dialog_box","is_open",allow_duplicate=True),
    Input("run_binded_rule","n_clicks"),
    Input("proceed_delete","n_clicks"),
    State({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"value"),
    prevent_initial_call = 'initial_duplicate',
)
def run_selected_rules(n_clicks,n_clicks_2,no_of_records):

    if ctx.triggered_id is None or(n_clicks is None and n_clicks_2 is None):
        raise PreventUpdate
    
    if ctx.triggered_id == 'run_binded_rule' :
        proc_name = 'run_one_field_rule' 
        refresh = no_update
    else :
        proc_name = 'delete_rule_binding'
        refresh = 0
    try:
        if len(main_app.binding_id_list) > 0:
            msg = ""
            for i in main_app.binding_id_list:
                
                main_app.cursor.callproc(proc_name,args=[i])
                final_result  = None
                latest_result = None
                for stored_result in main_app.cursor.stored_results():
                    latest_result= stored_result.fetchall()
                
                for result in latest_result:
                    final_result = result

                if final_result[0] == 200: 
                    header = "Success!!"
                    icon = "success"
                elif final_result[0] == 409:
                    header = "Warning"
                    icon = "warning"
                elif final_result[0] == 500:
                    header = "Internal Error"
                    icon = "warning"
                msg = msg + "\n"+ final_result[1]
        else :
            header = "Warning"
            icon = "warning"
            msg = "Please select a rule before running"
    except Exception as e:
        print(f"--------------{e} -------------")
        msg = msg + "\n" + "Error in SQL Execution.Please contact Support"
        header = 'Error!!'
        icon = "danger"
    duration = 3500
    main_app.binding_id_list=[]
    return msg,header,icon,duration,True,[False for i in range(len(no_of_records))],None,refresh,False


@main_app.app.callback(
    Output("rule_binding_page_heading","children",allow_duplicate=True),
    Output({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"value",allow_duplicate=True),
    Input(f"cb_all_{main_app.environment_details['rule_binding_table_id']}","value"),
    State({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"name"),
    prevent_initial_call='initial_duplicate',
)
def select_and_unselect_all_rulebindings(select_all,check_boxes):
        if select_all is None :
            raise PreventUpdate

        main_app.binding_id_list = []
        if select_all:
            for index in range(len(check_boxes)):
                main_app.binding_id_list.append(check_boxes[index][0]["RULE_BINDING_ID"])

        return f"hey there - {main_app.binding_id_list}",[select_all for i in range(len(check_boxes))]


@main_app.app.callback(
    Output("confirm_dialog_box","is_open"),
    Output("info_toast","children",allow_duplicate=True),
    Output("info_toast","header",allow_duplicate=True),
    Output("info_toast","icon",allow_duplicate=True),
    Output("info_toast","duration",allow_duplicate=True),
    Output("info_toast","is_open",allow_duplicate=True),
    Input("delete_binded_rule","n_clicks"),
    Input("cancel_delete","n_clicks"),
    prevent_initial_call = True
)
def open_close_modal(n_clicks,n_clicks_2):

    if ctx.triggered_id is None or n_clicks is None:
        raise PreventUpdate

    if len(main_app.binding_id_list)==0 :
        return no_update,"Select a rule to delete","Warning","warning",2000,True
    
    modal_open_or_close = ctx.triggered_id == 'delete_binded_rule'

    return modal_open_or_close,no_update,no_update,no_update,no_update,no_update