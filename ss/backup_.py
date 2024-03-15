import pandas as pd
from tkinter.filedialog import askopenfilename
from tkinter import *
from tkinter import ttk
import tkinter.filedialog as fd
from tkinter import messagebox
from itertools import product
from itertools import permutations
from itertools import chain
import numpy as np
import sqlite3
from timebudget import timebudget
print(ttk.__version__)
print(pd.__version__)

def Close():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        win.destroy()

def get_col_name(cases, months):
    col_name = []
    for e1, e2 in product(cases, months):
        col_name.append((str(e1) + str(e2)))
    return col_name


def get_temp_RH(df_temp_RH):
    df_lowest = pd.DataFrame()
    df_average = pd.DataFrame()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for i in range(12):  # 0-11 -> Jan-Dec
        M = i + 1
        # print(M)    #month
        # print(months[i])
        df = (df_temp_RH.loc[:, df_temp_RH.columns.str.endswith(months[i])])
        df_lowest_temp = df.loc[:, df.columns.str.contains("Lowest")]
        df_avg_temp = df.loc[:, df.columns.str.contains("Average")]
        df_lowest_temp.columns = ["Temperature", "Relative Humidity"]
        df_lowest_temp.insert(0, 'Hour', range(1, 25))
        df_lowest_temp.insert(0, 'Month', M)
        df_lowest = pd.concat([df_lowest, df_lowest_temp], ignore_index=True)

        df_avg_temp.columns = ["Temperature", "Relative Humidity"]
        df_avg_temp.insert(0, 'Hour', range(1, 25))
        df_avg_temp.insert(0, 'Month', M)
        df_average = pd.concat([df_average, df_avg_temp], ignore_index=True)
    return df_lowest, df_average

def export(df_result, filename):
    #df ready for export as M01, M02 worksheets in excel workbook

    writer = pd.ExcelWriter(f'{filename}.xlsx', engine='xlsxwriter')
    df_result.to_excel(writer, sheet_name='abc', merge_cells=True, index=False, freeze_panes=(3, 0))
    print("exported", filename)




def year_limit(year):
    """ Determine if inp string is a valid integer (or empty) and is no more
        than MAX_DIGITS long."""
    MAX_DIGITS = 4
    try:
        int(year)  # Valid integer?
    except ValueError:
        valid = (year == '')  # Invalid unless it's just empty.
    else:
        valid = (len(year) <= MAX_DIGITS)  # OK unless it's too long.

    if not valid:
        messagebox.showinfo('Entry error',
                                'Invalid input (should be {} digits)'.format(MAX_DIGITS),
                                icon=messagebox.WARNING)
    return valid

@timebudget
def step1_getmetdata():
    global df_lowest, df_average
    print(year.get())

    root = Tk()
    root.withdraw()
    filesopened = fd.askopenfilenames(parent=root, title='Choose the files')
    root.destroy()

    print(filesopened)  #1 excel file only

    df_temp_RH = pd.read_excel(filesopened[0], index_col=None, na_values=['NA'], sheet_name ='All', engine="openpyxl", skiprows = 1)
    pd.set_option('display.max_rows', None)

    # folderpath = filesopened[0].rsplit("/",1)[0]
    # print(folderpath)
    #

    ###preprocess
    df_temp_RH = df_temp_RH.round()  # round-off to nearest integer
    print(df_temp_RH)
    df_temp_RH = df_temp_RH.astype(int)
    print(df_temp_RH)

    ###Input Keys

    cases_lowest = ['RH_Lowest_', 'TEMP_Lowest_']
    cases_average = ['RH_Average_', 'TEMP_Average_']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    target_columns = ["Speed", "PC.4", "TAXI.4", "LGV3.4", "LGV4.4", "LGV6.4", "HGV7.4", "HGV8.4",
                      "PLB.4", "PV4.4", "PV5.4", "NFB6.4", "NFB7.4", "NFB8.4", "FBSD.4", "FBDD.4",
                      "MC.4", "HGV9.4", "NFB9.4"]  # "ALL", "ALL.1", "ALL.2", "ALL.3", "ALL.4"

    target_pollutants = ["Pollutant Name: Oxides of Nitrogen", "Pollutant Name: PM30", "Pollutant Name: PM10",
                         "Pollutant Name: PM2.5", "Pollutant Name: Nitrogen Dioxide"]

    colname_lowest = get_col_name(cases_lowest, months)
    colname_average = get_col_name(cases_average, months)

    # print(colname_lowest)  # col_name = columns at input excel worksheet to look for respective TEMP and RH at each hour
    ###Create df with temp, RH
    df_ = get_temp_RH(df_temp_RH)
    df_lowest = df_[0]
    df_average = df_[1]
    # print(df_lowest)
    #BOTH lowest and average data is ready and imported;

@timebudget
def step2_addspeed():
    global unique_speed
    global df_combinations
    file2 = fd.askopenfilename(parent=win, title='Choose the Speed file')
    if emission.get() == "running":
        df = pd.read_excel(file2, index_col=None, na_values=['NA'], sheet_name=f'Average Speed ({year.get()})', skiprows=2,
                           engine='openpyxl', usecols="F:AC")
        df = df.round()
        df = df.astype(int)

    elif emission.get() == "starting":
        #Time do something
        pass

    speed = df.apply(lambda col: col.unique())
    l = list(chain.from_iterable(speed))
    l = np.array(l)
    unique_speed = np.unique(l)
    # print(unique_speed)
    # print(df_average)

    speed = list(unique_speed)
    # data = {'Month': [1, 1, 1, 1], 'Hour': [1, 2, 3, 4], 'Temp': [15, 15, 15, 14], 'RH': [58, 58, 59, 59]}
    # df = pd.DataFrame(data=data)
    if mode.get().lower() == "average":
        records = df_average.to_records(index=False)
        lists = df_average.values.tolist()
    elif mode.get().lower() == "lowest":
        records = df_lowest.to_records(index=False)
        lists = df_lowest.values.tolist()
    else:
        print("RUN mode input is incorrect")
    # print(lists)
    result = list(records)
    # print(result)  # df

    # for v in itertools.product(speed, lists):
    #     print(v)

    newlist = [list(item) for item in product(lists, speed)]

    # print(newlist)
    df2 = pd.DataFrame(data=newlist, columns=["metdata", "Vehicle Speed"])
    # print("DF2", df2)
    df_combinations = pd.DataFrame(df2["metdata"].to_list(), columns=["Month", "Hour", "Temperature", "Relative Humidity"])
    df_combinations["Vehicle Speed"] = df2["Vehicle Speed"].to_numpy()

    # df_combinations.to_excel("combinations.xlsx")
    # print(df_combinations)

    # Add a Label widget to display file inputted
    label2 = Label(win, text="import", font='Aerial 11')
    label2.pack(side= TOP)
    label2.config(text="Template loaded: "+file2)

@timebudget
def step3_lookupdatabase():
    global df_db
    conn = sqlite3.connect('EMFAC_database.db')
    cur = conn.cursor()
    if emission.get() == "running":
        table = ["no2", "nox", "pm25", "pm10", "pm30"]

        df_db = pd.DataFrame()
        print(unique_speed)
        print("This step takes approximately 2 minutes...")
        count = 0
        for table_x in table:
            # Return all results of query
            # cur.execute(
            #     f"SELECT * FROM {table_x} WHERE (`Speed` ={tuple(unique_speed)}  AND `Emfac Year` = {year.get()})")
            # a = cur.fetchall()
            print(table_x, "extracting...")
            df_temp = pd.read_sql_query(
                f"SELECT * FROM {table_x} WHERE (`Vehicle Speed` IN {tuple(unique_speed)} AND `Emfac Year` = {year.get()})", conn)
            # df.insert(0, "Pollutant")
            # print("DF_TEMP:",df_temp)
            if count == 0:
                df_db = df_temp
                # print("AFTER UPDATE:", df_db)
                # df_db = df_db.join(df_temp, how="left", rsuffix="_"+table_x)
            else:
                df_db = pd.merge(df_db, df_temp, on = ["Emfac Version", "Emfac Year", "Temperature", "Relative Humidity", "Vehicle Speed"])
                # print("DF_DB after join:", df_db)
                # df_db = pd.concat([df_db, df])
            count += 1

    elif emission.get() == "starting":
        table = ["se_no2", "se_nox", "se_pm10", "se_pm25", "se_pm30"]

    # df_db.to_excel("database_overview.xlsx")
    # print(df_db.head(1000)) #running/starting data of all5 pollutants
    # Be sure to close the connection
    conn.close()


    # https://stackoverflow.com/questions/283645/python-list-in-sql-query-as-parameter

@timebudget
def step4_joindata():
    global df_resultforoutput
    listofreceivers = ["PCALL",
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
    lst = ["Month", "Hour", "Temperature", "Relative Humidity", "Vehicle Speed", "Emfac Version", "Emfac Year"]
    for x in ["no2", "nox", "pm25", "pm10", "pm30"]:
        lst = lst + [sub + x for sub in listofreceivers]

    if emission.get() == "running":
        df_resultforoutput = pd.merge(df_combinations, df_db, how='left', on= ["Temperature", "Relative Humidity", "Vehicle Speed"])
    else:
        df_resultforoutput = pd.merge(df_combinations, df_db, how='left', on= ["Temperature", "Relative Humidity", "Time"])

    df_resultforoutput.columns = lst
    filename = str(year.get())+"_"+str(mode.get())+"_"+str(emission.get())
    # export(df_resultforoutput, filename)
    df_resultforoutput.to_excel(f"{filename}.xlsx")
# Create an instance of tkinter frame or window
win = Tk()

# Set the geometry of tkinter frame
win.geometry("700x1000")


# store user input
year = StringVar()
mode = StringVar()
emission = StringVar()
# Enter frame
enter = ttk.Frame(win)
enter.pack(padx=40, pady=40, fill='x', expand=False)

# register year entry constrains
reg = win.register(year_limit)  # Register Entry validation function.

# year entry
year_label = ttk.Label(enter, text="Run Year:")
year_label.pack(fill=None, expand=False)

year_entry = ttk.Entry(enter, textvariable=year, validate='key', validatecommand=(reg, '%P'))  # text variable is stored in variable 'year', with constraints to ensure 4 digit number is entered
year_entry.pack(fill=None, expand=False)
year_entry.focus()
# mode entry
mode_label = ttk.Label(enter, text="Run Mode (lowest/average):")
mode_label.pack(fill=None, expand=False)
# mode_entry = ttk.Entry(enter, textvariable=mode, validate='key')  # text variable is stored in variable 'mode', no constraint
# mode_entry.pack(fill=None, expand=False)
# mode_entry.focus()

mode = StringVar(enter)
mode.set("lowest") # default value
mode_drop = OptionMenu(enter, mode,"lowest", "average")
mode_drop.pack()


emission_label = ttk.Label(enter, text="Emission Mode (running/starting):")
emission_label.pack(fill=None, expand=False)
# emission_entry = ttk.Entry(enter, textvariable=emission, validate='key')  # text variable is stored in variable 'mode', no constraint
# emission_entry.pack(fill=None, expand=False)
# emission_entry.focus()
emission = StringVar(enter)
emission.set("running") # default value
emission_drop = OptionMenu(enter, emission, "running", "starting")
emission_drop.pack()


# Destroy window when click cross
win.protocol("WM_DELETE_WINDOW", Close)

# Add a Label widget
label = Label(win, text="Enter the Year of Study, Run Mode, Emission Mode and proceed step-by-step below", font='Aerial 11')
label.pack(pady=5)


# Add a Button Widget
ttk.Button(win, text="RUN STEP1: Select the Excel File with RH and Temp Data", command=step1_getmetdata).pack(side= TOP, pady=10, ipady=20)

ttk.Button(win, text="RUN STEP2: Select the Speed file (Enter correct Year in user input)", command=step2_addspeed).pack(side= TOP, pady=20)

ttk.Button(win, text="RUN STEP3: Query data from database", command=step3_lookupdatabase).pack(side= TOP, pady=10, ipady=20)

ttk.Button(win, text="RUN STEP4: Lookup and Export Result as Excel", command=step4_joindata).pack(side= TOP, pady=10, ipady=20)




win.mainloop()

