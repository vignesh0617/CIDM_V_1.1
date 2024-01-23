from connections.MySQL import *
from datetime import datetime

sql_query = f'insert into comments (`request_id` , `comment_by` , `comment` , `time_stamp`) values (26,"test user","is this comment added with timestamp" ,"{datetime.now()}" )'

res = get_data_as_tuple(sql_query=sql_query)

print(res)