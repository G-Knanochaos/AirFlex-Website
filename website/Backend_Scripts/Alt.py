import pandas as pd
import numpy as np
from .AC_Calc import input_request as inp
from .AC_Calc import conversion as inp_conversion


def fan_Ques():
    AC_csv = pd.read_csv('AC data/AC_Cost_Data.csv')
    watts = rep_input("Enter the wattage of your fan ('not sure' if you don't know): ", int_only=True)
    state = rep_input(f'What state do you live in? ', ans=list(AC_csv['State'].values.flatten()), nns=True)
    if inp_conversion(watts):
        return watts, state
    filt = (AC_csv['Ftype'].str.lower() == rep_input(
        "Enter the type (handheld, table, ceiling, tower, box) of fan you have (not skippable): ",
        ans=['handheld', 'table', 'ceiling', 'tower', 'box'], nns=True))
    return AC_csv.loc[filt, 'Fwatts'].values.flatten(), state


def fan_price(state, type, watts, hours):
    AC_csv = pd.read_csv('website/Backend_Scripts/AC data/AC_Cost_Data.csv')
    filt = (AC_csv['Ftype'].str.lower() == type)
    if inp_conversion(watts):
        watts = AC_csv.loc[filt, 'Fwatts'].values.flatten()
    return round(float(watts) * float(AC_csv.loc[AC_csv['State'].str.lower() == state, 'CostKwh']) / 1000, 2) * hours


if __name__ == '__main__':
    watts, state = fan_Ques()
    print(f'Your fan costs {fan_price(state, watts)} cents per hour of operation.')
