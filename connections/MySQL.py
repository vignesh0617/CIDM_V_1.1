import mysql.connector as sql
from mysql.connector import errorcode
from callback_functions.backend_creation_functions import return_sql_queries_from_file
from callback_functions.main_app_class import main_app
import pandas as pd

def create_the_required_backend_tables(username,password):
    connector = sql.connect(
            user = main_app.environment_details['username'], 
            password = main_app.environment_details['password'], 
            host = main_app.environment_details['host'] ,
            autocommit =True) 
    cursor = connector.cursor()
    cursor.execute(f"create database {main_app.environment_details['database_name']}")
    cursor.execute(f"use {main_app.environment_details['database_name']}")
    queries = return_sql_queries_from_file()

    for table_name, query in queries.items():
        try : 
            cursor.execute(query)
        except Exception as e:
            print(f"\n\n\n======================Can not execute the below query\n\n {query}\n\n====================")
    
    return connector,cursor,True
    

#creates a backend connection with mysql connector and return the connection
def get_connection(username=main_app.environment_details['username'],password=main_app.environment_details['password']):
    try:
        connector = sql.connect(
            user = username, 
            password = password, 
            host = main_app.environment_details['host'] , 
            database = main_app.environment_details["database_name"],
            autocommit =True) 
        return connector,connector.cursor(),True
    except sql.Error as error :
        if (error.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            print("Invalid username/password")
            return None,None,False
        elif (error.errno == errorcode.ER_BAD_DB_ERROR) :
            print("Required backend database and tables not found, creating the requeried tables and database")
            # return create_the_required_backend_tables(username=username,password=password)
        else :
            print("Something unexpected happened. Contact support")
            return None,None,False
    
#gets tables data and returns it from the selected database as a dataframe obj
def get_data_as_data_frame(sql_query,cursor = None) -> pd.DataFrame:
    try :
        new_connector, new_cursor, flag = get_connection()
        new_cursor.execute(sql_query)
        fields = new_cursor.description
        data = new_cursor.fetchall()
        column_labels = [row[0] for row in fields]
        new_cursor.close()
        new_connector.close()
        return pd.DataFrame(data = data, columns= column_labels)
    except Exception as e :
        print(f'The sql query = {sql_query}')
        print('-----------------The exception is ---------------------\n',e)
        return 'Error'
        

main_app.connector, main_app.cursor, flag = get_connection() #connector,connector.cursor(),True



def get_data_as_tuple(sql_query:str):
    try :
        new_connector, new_cursor, flag = get_connection()
        new_cursor.execute(sql_query)
        res = new_cursor.fetchall()
        new_cursor.close()
        new_connector.close()
        return res
    except Exception as e :
        print(f'The sql query = {sql_query}')
        print('-----------------The exception is ---------------------\n',e)
        return 'Error'


# main_app.connector, main_app.cursor, flag = get_connection()
# cursor.execute(sql_query)
# fields = cursor.description
# data = cursor.fetchall()
# column_labels = [row[0] for row in fields]
# return pd.DataFrame(data = data, columns= column_labels)





