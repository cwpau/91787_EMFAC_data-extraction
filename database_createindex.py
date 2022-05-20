import sqlite3
from tkinter import *
import tkinter.filedialog as fd
from timebudget import timebudget

@timebudget  # Record how long this function takes
def importcsv(table1, table2):

    root = Tk()
    root.withdraw()
    dblocation = fd.askopenfilename(parent=root, title='Choose the files')   #askopenfilename = str, askopenfilenames = tuple
    root.destroy()

    if dblocation:
        print("DB loaded:",dblocation)

    else:
        dblocation="EMFAC_database.db"

    conn = sqlite3.connect(dblocation)
    c = conn.cursor()

    for t in table1:
        i = t+"_title"
        # p = f'''CREATE UNIQUE INDEX "{i}" ON "{t}" (
        # Emfac Year" ASC,
        # "Temperature" ASC,
        # "Relative Humidity" ASC,
        # "Vehicle Speed" ASC)'''
        # print(p)
        c.execute(f'''CREATE UNIQUE INDEX {i} ON {t} (
        "Emfac Year" ASC,
        "Temperature" ASC,
        "Relative Humidity" ASC,
        "Vehicle Speed" ASC)''')
    conn.commit()
    for t in table2:
        i = t+"_title"
        c.execute(f'''CREATE UNIQUE INDEX {i} ON {t} (
        "Emfac Year" ASC,
        "Temperature" ASC,
        "Time" ASC)''')

    conn.commit()
    # Be sure to close the connection
    conn.close()

if __name__ == "__main__":


    table1 = ["no2", "nox","pm10", "pm25", "pm30"]

    table2 = ["se_no2", "se_nox","se_pm10", "se_pm25", "se_pm30"]
    importcsv(table1, table2)