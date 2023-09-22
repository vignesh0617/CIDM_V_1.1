from dash import html, Output, Input,State,ALL,ctx
from dash.exceptions import PreventUpdate
from callback_functions.main_app_class import main_app
from callback_functions.custom_helpers import create_dash_table_from_data_frame
from connections.MySQL import get_data_as_data_frame
from plotly.express import pie,line
from callback_functions.side_filter_tab_function import *

@main_app.app.callback(
    
    Output({"type":f'rb_{main_app.environment_details["score_card_top_table_id"]}',"index":ALL},"value"),
    Output('score_card_binded_rules','children'),
    Output('trend_chart','figure'),
    Input({'type' : f"{main_app.environment_details['score_card_top_table_id']}_row_number",'index' : ALL},'n_clicks'),
    State({'type' : f"{main_app.environment_details['score_card_top_table_id']}_row_number",'index' : ALL},'key'),
    State({"type":f'rb_{main_app.environment_details["score_card_top_table_id"]}',"index":ALL},"name"),
)
def update_bottom_table1_failed_records(n_clicks,keys,key_for_radio_button,):


    if(ctx.triggered_id is None ):
        raise PreventUpdate
    
    rule_name = keys[ctx.triggered_id['index']]['RULE_NAME']
    table_name = keys[ctx.triggered_id['index']]['TABLE_NAME']
    column_name = keys[ctx.triggered_id['index']]['COLUMN_NAME']
    failed_data_table_name = keys[ctx.triggered_id['index']]['FAILED_DATA_TABLE_NAME']
    run_id = keys[ctx.triggered_id['index']]['LATEST_RUN_ID']


    # main_app.score_card_selected_rule = selected_rule

    sql_query = f'select * from {failed_data_table_name} where run_id = "{run_id}"'

    data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

    score_card_binded_rules_table = create_dash_table_from_data_frame(
            data_frame_original=data_frame,
            table_id= main_app.environment_details["score_card_bottom1_table_id"],
            key_col_number=int(main_app.environment_details["score_card_bottom1_table_primary_key_col_number"]),
            # col_numbers_to_omit= [ int(num) for num in main_app.environment_details['score_card_bottom1_table_col_numbers_to_omit'].split(',')],
            # primary_kel_column_numbers=[int(num) for num in main_app.environment_details["score_card_bottom1_table_primary_key_col_numbers"].split(",")],
            # action_col_numbers=[int(num) for num in main_app.environment_details['score_card_bottom1_table_col_action_col_number'].split(",")],
            )
    
    sql_query = f'select * from trend_chart_data where rule_name = "{rule_name}" and table_name = "{table_name}" and column_name = "{column_name}"'
    trend_data = get_data_as_data_frame(sql_query=sql_query , cursor = main_app.cursor)

    
    trend_chart = line(data_frame=trend_data,
                     x='DATE',
                     y='FAILED_RECORDS',
                     title = 'Trend Chart',
                     color_discrete_sequence = ['#FB2576'],
                    #  hover_data = ['PASSED_RECORDS','FAILED_RECORDS'],
                     width =615,
                     height=200)
    
    trend_chart.update_layout(margin=dict(l=20,r=20,t=40,b=20))
    
    trend_chart.update_xaxes(title='', visible=True, showticklabels=False)
    trend_chart.update_yaxes(title='', visible=True, showticklabels=True)
    trend_chart.update_layout(showlegend=False)
    trend_chart.update_layout(yaxis_range=[-5,trend_data['FAILED_RECORDS'].max()+10 if trend_data['FAILED_RECORDS'].max() != 0 else 100])
    
    return [True if ctx.triggered_id["index"] == i else False for i in range(len(key_for_radio_button))],score_card_binded_rules_table,trend_chart


