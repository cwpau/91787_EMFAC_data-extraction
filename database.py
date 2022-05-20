import sqlite3
from tkinter import *
import tkinter.filedialog as fd
from timebudget import timebudget


###load csv to sqlite3
import pandas as pd


conn = sqlite3.connect('EMFAC_database.db')
c = conn.cursor()
@timebudget  # Record how long this function takes
def importcsv():
    root = Tk()
    root.withdraw()
    filesopened = fd.askopenfilenames(parent=root, title='Choose the files')
    root.destroy()
    for files in filesopened:
        print(files)
        table_name = files.rsplit("/", 1)[1]   #no2_2024.csv    #se_no2_2024.csv
        table_name = table_name.partition(".")[0]  # no2_2024    #se_no2_2024
        table_name = table_name.rpartition("_")[0]  # no2   #se_no2
        print(table_name)
        if table_name.startswith("se"):
            df = pd.read_csv(files, usecols = columns_se)
            # df[["Relative Humidity"]] = df[["Relative Humidity"]].apply(pd.to_numeric())
        else:
            df = pd.read_csv(files, usecols = columns)
        # print(df.head(100))

        df.to_sql(name=table_name, con=conn, if_exists='replace', index=False)

        # return df, table_name

# def innerjoin():
#     c.execute("SELECT * FROM no2 INNER JOIN nox ON (no2.`Time`= nox.`Time` AND no2.`Emfac Version`= nox.`Emfac Version` \
# AND no2.`Emfac Year`= nox.`Emfac Year` AND no2.`Emfac Version`= nox.`Emfac Version` AND no2.`Temperature` = nox.`Temperature`\
# AND no2.`Relative Humidity`=nox.`Relative Humidity`)")
#     a = c.fetchall()


columns = ["Emfac Version","Emfac Year","Temperature","Relative Humidity","Vehicle Speed",
           "PCALL",
           "TAXIALL",
           "LGV3ALL",
           "LGV4ALL",
           "LGV6ALL",
           "HGV7ALL",
           "HGV8ALL",
           "PLBALL",
           "PV4ALL",
           "PV5ALL",
           "NFB6ALL",
           "NFB7ALL",
           "NFB8ALL",
           "FBSDALL",
           "FBDDALL",
           "MCALL",
           "HGV9ALL",
           "NFB9ALL"]

columns_se = ["Emfac Version","Emfac Year","Temperature","Relative Humidity","Time",
           "PCALL",
           "TAXIALL",
           "LGV3ALL",
           "LGV4ALL",
           "LGV6ALL",
           "HGV7ALL",
           "HGV8ALL",
           "PLBALL",
           "PV4ALL",
           "PV5ALL",
           "NFB6ALL",
           "NFB7ALL",
           "NFB8ALL",
           "FBSDALL",
           "FBDDALL",
           "MCALL",
           "HGV9ALL",
           "NFB9ALL"]

output = importcsv()

# innerjoin()

# df = output[0]
# table_name = output[1]
# df.to_sql(name=table_name,con=conn,if_exists='replace',index=False)
conn.commit()
# Be sure to close the connection
conn.close()