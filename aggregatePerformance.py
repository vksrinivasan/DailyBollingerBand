import numpy as np
import pandas as pd
import pickle
import os.path

set_current = set()
df_current = None

def saveIntermediate(dates, returns):
    df_temp = pd.DataFrame()
    df_temp['Date'] = dates
    df_temp['Returns'] = returns
    df_temp.set_index(['Date'])
    str_finalName = "DailyStratRets_longshort" + str(dates[-1]) + ".csv"
    df_temp.to_csv(str_finalName)


def loadPickle(name):
    output = pickle.load(open('C:\\Users\\Vyas\\Desktop\\Results\\' + name + '.p', 'rb'))
    new_df = pd.DataFrame(output['Returns'], index=output['Dates'],columns=[name.replace('-','_')])
    return new_df

def cleanDF(set_toDel):
    global df_current
    for name in set_toDel:
        name = name.replace('-','_')
        if name not in df_current:
            continue
        df_current.drop(name, axis=1, inplace=True)

def addToDF(set_toAdd):
    global df_current
    for name in set_toAdd:
        assert(name not in df_current) # just to check

        if not os.path.isfile('C:\\Users\\Vyas\\Desktop\\Results\\' + name + '.p'):
            print 'missing'
            continue

        # Load the pickle we need
        df_nameToAdd = loadPickle(name)

        # Join the stock's data by index (i.e. date)
        df_current = pd.merge(df_current, df_nameToAdd, how='left', left_index=True, right_index=True)

def getReturns():
    ls_returns = []
    global df_current
    global set_current
    index = 0
    with open('GetConstituents\\DailyAPIFileFinal_v.csv', 'r') as cons:
        for line in cons:
            data = line.replace('\n','').replace('\t','').split(',')
            date = int(data[0])

            # Print the date just so we have it
            print('----------------' + str(date) + '----------------')

            set_symbols = set(data[1:501])

            # Figure out which pickle files need to be read in/what existing data columns we can delete
            set_toDel = set_current - set_symbols
            set_toAdd = set_symbols - set_current

            # Remove unused columns/add in needed ones
            cleanDF(set_toDel)
            addToDF(set_toAdd)

            # calculate returns for the day (equal weighted across all names)
            ls_returns.append(df_current.ix[date].mean())

            # Update set_current
            set_current = set_symbols

            index += 1
            if(index%252==0):
                saveIntermediate(df_current.index.values[:index], np.array(ls_returns))

            # if(index%20 == 0):
            #     break

    return np.array(ls_returns)

def getDates():
    ls_dates = []
    with open('GetConstituents\\DailyAPIFileFinal_v.csv', 'r') as cons:
        for line in cons:
            data = line.replace('\n','').replace('\t','').split(',')
            date = int(data[0])
            ls_dates.append(date)
    return ls_dates

def main():
    ls_dates = getDates()
    global df_current
    df_current = pd.DataFrame(index=ls_dates)
    np_returns = getReturns()

    final_df = pd.DataFrame()
    final_df['Date'] = ls_dates[:np_returns.__len__()]
    final_df['Returns'] = np_returns
    final_df.set_index(['Date'])

    final_df.to_csv('DailyStratRets_longshort.csv')

if __name__ == "__main__":
    main()