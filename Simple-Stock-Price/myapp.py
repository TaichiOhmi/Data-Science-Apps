import yfinance as yf
import streamlit as st
import pandas as pd

# Webアプリ

# HTMLとか書かずにマークダウンの書き方でフロントエンドを描ける
# タイトル等
st.write("""
# Simple Stock Price App

Shown are the stock **closing** price and ***volume*** of Google!

""")

tickerSymbol = 'GOOGL'
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period='id', start='2010-5-31', end='2022-7-15')

st.write("""
## Closing Price
""")
st.line_chart(tickerDf.Close)
st.write("""
## Volume Price
""")
st.line_chart(tickerDf.Volume)