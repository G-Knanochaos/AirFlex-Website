from matplotlib import pyplot as plt
from AC_Calculator import rep_input
import pandas as pd
import numpy as np
from datetime import datetime
import csv


# ---[CSV INTERACTION]---


def init_csv(user):
    with open(f'AC data/{user}_data.csv', 'w', newline='') as user_csv:
        writer = csv.writer(user_csv)
        writer.writerows([['Date', 'Hours', 'Temperature', 'Cost']])


def write_csv(user, hours, temp, cost, inpdate=None):
    with open(f'AC data/{user}_data.csv', 'a', newline='') as user_csv:
        writer = csv.writer(user_csv)
        if inpdate:
            writer.writerow([pd.to_datetime(inpdate, format='%Y-%m-%d'), hours, temp, cost])
        else:
            writer.writerow([datetime.today().strftime('%Y-%m-%d'), hours, temp, cost])


# ---[GRAPHING]---

def graph(vals, user):
    user_csv = pd.read_csv(f'AC data/{user}_data.csv')
    x = user_csv['Date'].tolist()
    for val in vals:
        plot_graph = plt.figure(f"AC {val} Graph")
        plt.xlabel("Date")
        plt.ylabel(val)
        plt.title(f'AC {val} Graph')
        plt.plot(x, [user_csv.loc[(user_csv['Date'] == date), val] for date in x], label=val, marker='o', linewidth='3')
        plt.legend()
        plt.show()


# ---[MAIN]---

def main():
    init_csv('Christopher')
    write_csv('Christopher', '8', '65', '10', inpdate='2019-08-03')
    write_csv('Christopher', '7', '68', '7', inpdate='2020-08-03')
    write_csv('Christopher', '5', '69', '6', inpdate='2021-08-03')
    graph(['Hours', 'Temperature', 'Cost'], 'Christopher')


if __name__ == '__main__':
    main()
