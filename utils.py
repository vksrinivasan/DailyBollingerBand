# Author: Vyas K. Srinivasan
# Utility Code

import pandas as pd
import numpy as np
from os import listdir
import pickle

# Get data from Premium Data extracted File
def getData(str_data_folder=r'C:\Users\Vyas\OneDrive\CS8903\Clean', str_ticker='AZO', str_freq='D'):
    str_filePath = str_data_folder + "\\" + str_ticker + ".csv"
    df_prices_full = pd.read_csv(str_filePath, sep=",")

    df_prices_period = getTimeScale(df_prices_full, str_freq)

    return df_prices_period

# Segment out the data we need
def getTimeScale(df_prices, str_freq):

    # Someone (probably me later) should throw some logic in here to segment out the data for monthly/weekly
    if(str_freq=='D'):
        return df_prices

def getListOfStockNames(str_data_folder=r"D:\ListedStockHistory\Clean\US\AMEX"):
    ls_names = listdir(str_data_folder)
    ls_names = [x.replace('.csv', '') for x in ls_names]
    return ls_names

def writeToDisk(dict_results, name, str_data_folder="D:\ListedStockHistory\Clean\US\AMEX"):
    str_outName = str_data_folder + "//" + name + '.p'
    pickle.dump(dict_results, open(str_outName, "wb"))

def main():
    getData()

if __name__ == "__main__":
    main()