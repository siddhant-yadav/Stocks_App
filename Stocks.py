import yfinance as yf
import streamlit as st
import pandas as pd 
import numpy as np 
from datetime import datetime

now = datetime.now() # current date and time

def go_back(x):
    # now = datetime.now() # current date and time
    yrs = int(now.strftime("%Y")) - int(x/12)
    
    if(int(now.strftime("%m")) > int(x%12)):                          
        months = int(now.strftime("%m")) - int(x%12)
    else:
        months = int(now.strftime("%m")) - int(x%12) + 12
        yrs -= 1

    day = now.strftime("%d")    

    string_date = f"{yrs}-{months}-{day}"
    return string_date


st.write("""
# Simple Stock Price App
Shown are the stock closing price and volume of Google!
""")


# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75

Dataframe = pd.read_csv('sp_500_stocks.csv')
tickerSymbol = st.selectbox('Which Company Would you like to Analyse',Dataframe)


today_date = now.strftime("%Y-%m-%d")
months_to_go_back = st.slider("Months")

if(months_to_go_back == 0):
    From_date = now.strftime("%Y-%m-1")
else:    
    From_date = go_back(months_to_go_back)

st.write("From: ",From_date,"To: ",today_date)




choice_data = st.radio('What Data do you need?',["High_vs_Low","Profit A_vs_B"])



#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start=From_date, end=today_date)
# Open	High	Low	Close	Volume	Dividends	Stock Splits

Dataframe2 = Dataframe[Dataframe['Ticker'] != tickerSymbol]

if(choice_data == "High_vs_Low"):
    st.write("This is",tickerSymbol)
    data_H_L = pd.DataFrame({"High":tickerDf.High,"Low":tickerDf.Low})
    st.line_chart(data_H_L)

    # profit = pd.DataFrame(tickerDf.Close - tickerDf.Open)
    # st.area_chart(profit)



if(choice_data == "Profit A_vs_B"):
    tickerSymbol2 = st.selectbox('Which Company Would you like to Analyse',Dataframe2)
    # tickerSymbol2 = 'AAPL'
    tickerData2 = yf.Ticker(tickerSymbol2)
    tickerDf2 = tickerData2.history(period='1d', start=From_date, end=today_date)

    profit1 = tickerDf.Close - tickerDf.Open
    profit2 = tickerDf2.Close - tickerDf2.Open
    
    Data_comp = pd.DataFrame({f"{tickerSymbol}":(tickerDf.High + tickerDf.Low)/2,f"{tickerSymbol2}":(tickerDf2.High + tickerDf2.Low)/2})
    st.line_chart(Data_comp)

    data_Close = pd.DataFrame({tickerSymbol: profit1,tickerSymbol2:profit2})
    st.line_chart(data_Close)
# st.line_chart(tickerDf.High)

