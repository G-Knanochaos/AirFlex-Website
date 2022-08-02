import pandas as pd
import numpy as np

AC_csv = pd.read_csv('AC_Cost_Data.csv')


def rep_input(inp, ans=None, int_only=False, rep=False, nns=False):
    if rep and ans and nns:
        print(f'Please input one of the valid answers : {ans}')
    elif rep and ans and not nns:
        print(f'Please input one of the valid answers : {ans + ["not sure"]}')
    elif rep and int_only:
        print(f'Please input an integer.')
    res = input(inp).lower()
    if int_only:
        try:
            return float(res)
        except ValueError:
            return res if res == 'not sure' else rep_input(inp, int_only=True, rep=True)
    return res if not ans and not int_only or res in [x.lower() for x in ans if isinstance(x, str)] + ['not sure'] and \
                  not nns else res if res in [x.lower() for x in ans if isinstance(x, str)] else rep_input(inp, ans=ans,
                                                                                                           rep=True,
                                                                                                           nns=nns)


def conversion(val, conversion, l_bound=None, u_bound=None):
    if val == 'not sure':
        return False
    if l_bound and u_bound:
        if val > u_bound or val < l_bound:
            i = rep_input(
                'Your value was deemed unreasonablyt high or low by the system. This failsafe was put in place '
                'to minimize the risk of entering a mistaken value and skewing the results. Input "y" to move'
                'on to the next question, input "n" to use this value anyway: ', ans=['y', 'n'], nns=True)
            return val * conversion if i == 'n' else False
    return val * conversion


def KwH_Ques():
    BTU = rep_input("Enter the BTU of your air conditioner ('not sure' if you don't know): ", int_only=True)
    if conversion(BTU, 1 / 12000, 1000, 80000):
        return [conversion(BTU, 1 / 12000), None]
    watts = rep_input("Enter the wattage of your air conditioner ('not sure' if you don't know): ", int_only=True)
    if conversion(watts, 1 / 1000, 83, 6667):
        return [conversion(watts, 1 / 1000), None]
    est_df = pd.DataFrame(AC_csv.loc[(AC_csv['Type'] == rep_input(
        "Enter the type (central, window unit, mini split) of air conditioner you have (not skippable): ",
        ans=['central', 'window unit', 'mini_split'], nns=True)) & (AC_csv['Size'] == rep_input(
        "Enter the size (small, medium, large) of your air conditioner (not skippable): ",
        ans=['small', 'medium', 'large'], nns=True)), ['KwhPH', 'GOT']])
    return est_df.values.flatten()


def csv_loc(csv):
    try:
        city = rep_input("What is the nearest major city to you (preferably >100 miles): ", nns=True)
        date = rep_input("What month of the year is it (enter a number)? ", ans=[str(n + 1) for n in range(12)],
                         nns=True)
        filt = (csv['Station.City'] == city) & (csv['Date.Month'] == int(date))
        return csv.loc[filt, ['Data.Temperature.Avg Temp', 'Data.Temperature.Max Temp']]
    except:
        print("Make sure the city you entered is 1) a city (not a county/state) and 2) doesn't contain spelling errors")
        return csv_loc(csv)


def Price_Ques(kwh, tense):
    tense_dict = {'present': ['was', 'today', 'did'], 'past': ['is', 'most days', 'do']}
    t1, t2, t3 = tense_dict[tense]
    EER = rep_input(
        "What is the EER (energy efficiency ratio) of your air conditioner : format w/ 1 decminal point ('not sure' "
        "if you don't knot): ", ans=[str(n / 2) for n in range(12, 25)])
    if EER == 'not sure':
        EER = '8.5'
    hours = rep_input(f'How many hours {t1} your air conditioner on {t2}? ', int_only=True, nns=True)
    temp = rep_input(f'What temperature {t3} you set your air conditioner to (F)? ', int_only=True, nns=True)
    state = rep_input(f'What state do you live in? ', ans=list(AC_csv['State'].values.flatten()), nns=True)
    use_csv = rep_input("Would you like to use average temperature data for your area (recommended unless there is "
                        "abnormally high or low weather conditions at the moment in your area) (y/n): ", ans=['y', 'n'],
                        nns=True)
    W_csv = pd.read_csv('WBC.csv')
    W_csv['Station.City'] = W_csv['Station.City'].str.lower()
    if use_csv == 'y':
        avg_max = csv_loc(W_csv)
        avgs = [avg_max['Data.Temperature.Avg Temp'].mean(), avg_max['Data.Temperature.Max Temp'].mean()]
        avg = (avgs[0] + (avgs[1] * 5)) / 6
    elif use_csv == 'n':
        avgs = [rep_input('What was the average temperature today? ', int_only=True, nns=True),
                rep_input('What was the high temperature today? ', int_only=True, nns=True)]
        avg = ((avgs[0] + (avgs[1] * 5))) / 6
    AC_csv['State'] = AC_csv['State'].str.lower()
    print(hours)
    print((AC_csv.loc[AC_csv['Dchange'] == int(avg - temp), 'Dmult']).values.flatten())
    print(AC_csv.loc[AC_csv['State'] == state, 'CostKwh'].values.flatten())
    print(AC_csv.loc[AC_csv['EER'] == float(EER), 'Emult'].values.flatten())
    return hours * float(AC_csv.loc[AC_csv['Dchange'] == int(avg - temp), 'Dmult']) * float(
        AC_csv.loc[AC_csv['State'] == state, 'CostKwh']) * float(
        AC_csv.loc[AC_csv['EER'] == float(EER), 'Emult']) * float(kwh) / 100


if __name__ == '__main__':
    kwhph = KwH_Ques()
    if kwhph[1]:
        print(f'Your air conditioner spends {kwhph[0]} kWh hourly, give or take {kwhph[1]} kWh.')
    if not kwhph[1]:
        print(f'Your air conditioner spends aproximatley {kwhph[0]} kWh hourly.')
    print(f"You spent aproximatley \n${Price_Ques(kwhph[0], 'present')}\n today on air conditioning.")
