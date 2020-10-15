import pandas as pd
import numpy as np
from locale import atof, setlocale, LC_NUMERIC
from matplotlib import pyplot as plt
import datetime, pprint
import pprint

def get_year(yearlist):
    #parameter: List of years (int).
    #Returns a dictionary whith the year as key, and the Total Cost accumulated for each month of that year.
    #If there are no datapoints for a specific month, 0.0 is returned.
    returndict = {}
    
    for YEAR in yearlist:
        dictionary = {}

        for i, row in df.iterrows():
            for month in range(1,13):
                if row["Deadline"].isocalendar()[0] == YEAR:
                    if row["Deadline"].month == month:
                        if row["Job Type"] == "UEB ohne 100" or row["Job Type"] == "UEB mit 100":
                            try:
                                dictionary[month] += (df["Total Cost [€]"][i])
                            except KeyError:
                                dictionary[month] = (df["Total Cost [€]"][i])
                        
                        elif row["Job Type"] == "Translation":
                            try:
                                dictionary[month] += (df["Total Cost [€]"][i])
                            except KeyError:
                                dictionary[month] = (df["Total Cost [€]"][i])

                        elif row["Job Type"] == "revision":
                            try:
                                dictionary[month] += (df["Total Cost [€]"][i])
                            except KeyError:
                                dictionary[month] = (df["Total Cost [€]"][i])

        y_axis = []
        for i in range(1,13):
            y_axis.append(dictionary.get(i, 0.0))
        
        returndict[YEAR] = y_axis
    
    return returndict

#Setlocale gjør at vi kan lage floats når desimalene skilles av komma i stedet for punktum.
setlocale(LC_NUMERIC, '')

YEARS = [2018, 2019, 2020]
PROVIDER = "Ole"
YEARS_STR = []
for year in YEARS:
    YEARS_STR.append(str(year))


df = pd.read_csv("jobber_ole_all.csv", encoding="UTF-8")

#Hent ut de to relevante spaltene
df = df[["Job Type", "Deadline", "Total Cost [€]"]]

#Endre CEST til CET (Er uansett kun interessert i måneder)
for index, row in df.iterrows():
    if row["Deadline"].endswith("CEST"):
        row["Deadline"] = row["Deadline"][:-4] + "CET"

#Gjør feltene i Deadline om til date_time-typer
df["Deadline"] = pd.to_datetime(df["Deadline"], format=r"%d.%m.%Y %H:%M CET")

#Gjør strenger om til floats
for i, row in df.iterrows(): 
    df["Total Cost [€]"][i] = atof(row["Total Cost [€]"])

x_axis = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
y_axisdict = get_year(YEARS)

tbprinted = {}
for key, value in y_axisdict.items():
    tbprinted[key] = (sum(value) / 12)

pprint.pprint(tbprinted)

x_indexes = np.arange(len(x_axis))
width = 0.25

plt.title("Total Cost for " + PROVIDER + " for " + "/".join(YEARS_STR))
plt.style.use("fivethirtyeight")
# plt.bar(x_indexes - width, y_axisdict[YEARS[0]], width=width, label=YEARS_STR[0])
# plt.bar(x_indexes, y_axisdict[YEARS[1]], width=width, label=YEARS_STR[1])
# plt.bar(x_indexes + width, y_axisdict[YEARS[2]], width=width, label=YEARS_STR[2])
plt.plot(x_indexes, y_axisdict[YEARS[0]], label=YEARS_STR[0])
plt.plot(x_indexes, y_axisdict[YEARS[1]], label=YEARS_STR[1])
plt.plot(x_indexes, y_axisdict[YEARS[2]], label=YEARS_STR[2])
plt.legend()
plt.ylabel("NOK")
plt.xticks(ticks=x_indexes, labels=x_axis)
plt.xlabel("Week Number")
plt.show()

    
    
