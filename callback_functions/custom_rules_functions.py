from dash import Input,Output,State,ctx,no_update
from dash.exceptions import PreventUpdate
from callback_functions.main_app_class import main_app


def validate_custom_rules_form(requesting_user,user_email,request_type,business_desc_sql,status):

    user_flag = requesting_user is not None and len(requesting_user.strip()) >5 
    email_flag = user_email is not None and len(user_email.strip()) != 0 and user_email.find("@") != -1 and user_email.find(".com") != -1 and (user_email.find(".com") - user_email.find("@") != 1)
    type_flag = request_type is not None and len(request_type.strip()) != 0 
    sql_flag = business_desc_sql is not None and len(business_desc_sql.strip()) != 0 
    status_flag  = status is not None and len(status.strip()) != 0 

    individual_flags = dict(user_flag = user_flag,email_flag=email_flag,type_flag=type_flag,sql_flag=sql_flag,status_flag=status_flag)
    final_flag = user_flag and email_flag and type_flag and status_flag

    return individual_flags,final_flag

@main_app.app.callback(
    Output("info_toast","children",allow_duplicate=True),
    Output("info_toast","header",allow_duplicate=True),
    Output("info_toast","icon",allow_duplicate=True),
    Output("info_toast","duration",allow_duplicate=True),
    Output("info_toast","is_open",allow_duplicate=True),
    Output("requesting_user","valid",allow_duplicate=True),
    Output("requesting_user","invalid",allow_duplicate=True),
    Output("user_email","valid",allow_duplicate=True),
    Output("user_email","invalid",allow_duplicate=True),
    Output("request_type","valid",allow_duplicate=True),
    Output("request_type","invalid",allow_duplicate=True),
    Output("business_desc_sql","valid",allow_duplicate=True),
    Output("business_desc_sql","invalid",allow_duplicate=True),
    Output("status","valid",allow_duplicate=True),
    Output("status","invalid",allow_duplicate=True),
    Input("cudf_submit_btn","n_clicks"),
    State("requesting_user","value"),
    State("user_email","value"),
    State("request_type","value"),
    State("business_desc_sql","value"),
    State("status","value"),
    prevent_initial_call = True
)
def open_close_modal(n_clicks,requesting_user,user_email,request_type,business_desc_sql,status):




    if ctx.triggered_id is None or n_clicks is None:
        raise PreventUpdate
    
    print('Entered into func')
    individual_flags,all_fields_validated = validate_custom_rules_form(requesting_user,user_email,request_type,business_desc_sql,status)

    if all_fields_validated:
        try :
            sql_query = f'insert into custom_rules_request (`REQUESTING_USER`,`USER_EMAIL`,`REQUEST_TYPE`,`DESCRIPTION/SQL`,`STATUS`) values ("{requesting_user.strip()}","{user_email.strip()}","{request_type.strip()}","{business_desc_sql.strip()}","{status.strip()}")'
            main_app.cursor.execute(sql_query)
            res = main_app.cursor.fetchall()
            print('Inserted successfully')
            return "Request Submitted","Success","success",5000,True,individual_flags["user_flag"],not(individual_flags["user_flag"]),individual_flags["email_flag"],not(individual_flags["email_flag"]),individual_flags["type_flag"],not(individual_flags["type_flag"]),individual_flags["sql_flag"],not(individual_flags["sql_flag"]),individual_flags["status_flag"],not(individual_flags["status_flag"])
        except Exception as e:
            print('---------------------------\n',str(e).split(":")[1],str(e).split(":")[0] == '1062 (23000)')
            msg = 'This request is already submitted by another user' if str(e).split(":")[0] == '1062 (23000)' else str(e)
            return msg,"Warning","warning",5000,True,individual_flags["user_flag"],not(individual_flags["user_flag"]),individual_flags["email_flag"],not(individual_flags["email_flag"]),individual_flags["type_flag"],not(individual_flags["type_flag"]),individual_flags["sql_flag"],not(individual_flags["sql_flag"]),individual_flags["status_flag"],not(individual_flags["status_flag"])
    

    return "Fill all details","Warning","warning",5000,True,individual_flags["user_flag"],not(individual_flags["user_flag"]),individual_flags["email_flag"],not(individual_flags["email_flag"]),individual_flags["type_flag"],not(individual_flags["type_flag"]),individual_flags["sql_flag"],not(individual_flags["sql_flag"]),individual_flags["status_flag"],not(individual_flags["status_flag"])