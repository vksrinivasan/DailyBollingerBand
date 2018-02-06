# Author: Vyas K. Srinivasan
# Bollinger Band Code - Calculate Bollinger Band

import pandas as pd
import numpy as np

from utils import getData

# Helper function to get rolling sum for a given lookback
def getSMA(df_data, lookback=20):
    return df_data['Close'].rolling(lookback).mean().values

# Helper function to get rolling std for a given lookback
def getRollStd(df_data, lookback=20):
    return df_data['Close'].rolling(lookback).std().values

# Helper function to get Bostian Volume Intensity
def getBostian(df_data, lookback=20):
    np_dailyBostian = df_data['Volume']*(((2*df_data['Close'].values)-df_data['High'].values-df_data['Low'].values)/ \
                      (df_data['High'].values-df_data['Low'].values))

    # just create a dataframe to get easy access to rolling
    df_temp = pd.DataFrame(np_dailyBostian)
    return np.squeeze(df_temp[[0]].rolling(lookback).sum().values)



# Outputs np array of trading decisions that can be read by a market simulator
def getPredictions(df_data, lookback):
    np_prices = df_data['Close'].values

    np_sma = getSMA(df_data, lookback)
    np_rstd = getRollStd(df_data, lookback)
    np_vInd = getBostian(df_data, lookback)

    np_low_band = np_sma - (2*np_rstd)
    np_high_band = np_sma + (2*np_rstd)

    np_decisions = np.zeros((np_vInd.shape[0]))

    # Now follow the rules outlined by Bollinger:
    # (1) Buy if we tag the lower band and indicator is positive - Encoded as 1
    # (2) Sell if we tag the upper band and the indicator is negative - Encoded as -1
    # Note: Do nothing is encoded as 0

    i = 0 # There might be a better way to do this. I need to index into np_decisions
    for price, lb, hb, volume in zip(np_prices, np_low_band, np_high_band, np_vInd):
        if(price <= lb and volume > 0):
            np_decisions[i] = 1
            i = i + 1
            continue
        if(price >= hb and volume < 0):
            np_decisions[i] = -1
            i = i + 1
            continue

        if(i != 0):
            np_decisions[i] = np_decisions[i-1]
        i = i + 1

    return np_decisions



def main():
    df_data = getData()
    getPredictions(df_data,20)

if __name__ == "__main__":
    main()

