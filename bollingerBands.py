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

def getBollingerBandIndicator(df_data, lookback, band_width=2):
    np_prices = df_data['Close'].values
    np_sma = getSMA(df_data, lookback)
    np_rstd = getRollStd(df_data, lookback)

    np_top_bb_band = np_sma + (band_width*np_rstd)
    np_bottom_bb_band = np_sma - (band_width*np_rstd)

    np_bbp = (np_prices - np_bottom_bb_band) / (np_top_bb_band - np_bottom_bb_band)

    return np_bbp

def getPositions(np_bbp, volume_indicator):
    np_decisions = np.zeros((np_bbp.shape[0]))
    i = 0
    for bbp, vi in zip(np_bbp, volume_indicator):
        if(bbp < 0.0 and vi > 0.0):
            np_decisions[i] = 1
            i = i + 1
            continue
        if(bbp > 1.0 and vi < 0.0):
            np_decisions[i] = 0
            i = i + 1
            continue

        if(i != 0):
            np_decisions[i] = np_decisions[i-1]
        i = i + 1
    return np_decisions

def getPositions_bOnly(np_bbp):
    np_decisions = np.zeros((np_bbp.shape[0]))
    i = 0
    for bbp in np_bbp:
        if(np.isnan(bbp)):
            i = i + 1
            continue
        if(bbp < 0.0):
            np_decisions[i] = 1
            i = i + 1
            continue
        if(bbp > 1.0):
            np_decisions[i] = -1
            i = i + 1
            continue
        if(i != 0):
            np_decisions[i] = np_decisions[i-1]
        i = i + 1
    return np_decisions

def main():
    df_data = getData()
    np_bbp = getBollingerBandIndicator(df_data, 20)
    np_vi = getBostian(df_data, 20)
    np_positions = getPositions(np_bbp, np_vi)

if __name__ == "__main__":
    main()

