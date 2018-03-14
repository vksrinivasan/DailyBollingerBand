# Author: Vyas K. Srinivasan
# Aggregator

import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime
import bisect
import calendar
from os import listdir
from PDsymbols import get_symbols
from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR
import pickle

def createSSD(pathName="C:\\Users\\Vyas\\Desktop\\Results"):
    ls_names = listdir(pathName)
    ls_names = [x.replace('.p', '') for x in ls_names]

    dict_ss = {}

    for name in ls_names:
        ls_temp = name.split('-')
        dt_temp = None
        if(ls_temp.__len__()==1):
            dt_temp = dt.datetime(2018,03,04)
        else:
            if(not ls_temp[1].isdigit()):
                continue
            ls_temp[1] = ls_temp[1][:6]
            set_monthRange = calendar.monthrange(int(ls_temp[1][:4]), int(ls_temp[1][4:]))
            dt_temp = datetime.strptime(ls_temp[1]+str(set_monthRange[1]), "%Y%m%d")

        if(ls_temp[0] not in dict_ss.keys()):
            dict_ss[ls_temp[0]] = []
        bisect.insort(dict_ss[ls_temp[0]], dt_temp)

    return dict_ss


def aggregateResults(dateRange, SSD):
    np_numStocks = np.zeros(dateRange.__len__())
    np_returns = np.zeros(dateRange.__len__())

    index = 0

    for date in dateRange:
        # This is such an unbelievably inefficient way to do this -
        # I am literally going through each day and then one by one
        # going through the io of reading each stock's pickle file and
        # updating my return calculation

        # It would definitely be better to just just one pickle file for all
        # the days where it is relevant, but for now I'm not doing that
        print(date)
        ls_stocks = get_symbols(date)
        temp_numStocks = ls_stocks.__len__()
        if(temp_numStocks==1 and ls_stocks[0]=="No symbols for this date"):
            pass
        else:
            np_numStocks[index] = temp_numStocks

            for stock in ls_stocks:
                dict_results = pickle.load(open("C:\\Users\\Vyas\\Desktop\\Results\\" + stock + ".p", "rb"))
                aaa = 5

        index = index + 1



def daterange(start_date, end_date):
  return rrule(DAILY, dtstart=start_date, until=end_date, byweekday=(MO,TU,WE,TH,FR))

def main():
    start_date = dt.datetime(1964,03,9)
    end_date = dt.datetime(2017,12,31)
    dateRange = daterange(start_date, end_date)
    stock_startDict = createSSD(pathName="C:\\Users\\Vyas\\Desktop\\Results")

    total_results = aggregateResults([x for x in dateRange], stock_startDict)

if __name__ == "__main__":
    main()