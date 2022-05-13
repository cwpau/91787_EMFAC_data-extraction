import sqlite3
from timebudget import timebudget
###load csv to sqlite3
import pandas as pd

@timebudget
def sql_export(year, Temp, RH):
    conn = sqlite3.connect('EMFAC_database.db')
    cur = conn.cursor()
    df = pd.DataFrame()
    if emission.get() == "running":
        table = ["no2","nox", "pm25", "pm10", "pm30"]

        for table_x in table:
            # Return all results of query
            cur.execute(f"SELECT * FROM {table_x} WHERE (`Speed` ={tuple(unique_speed)}  AND `Emfac Year` = {year.get()})")
            a = cur.fetchall()

            df_temp = pd.read_sql_query(f"SELECT * FROM {table_x} WHERE (`Speed` ={tuple(unique_speed)} AND `Emfac Year` = {year.get()})", conn)    #correct data of 1 pollutant
            df.join(df_temp, how="inner", on =("Temperature", "Relative Humidity", "Vehicle Speed"))


    elif emission.get() == "starting":
        table = ["se_no2", "se_nox", "se_pm10", "se_pm25", "se_pm30"]
        pass
    # Be sure to close the connection
    conn.close()
    return df
# https://stackoverflow.com/questions/283645/python-list-in-sql-query-as-parameter