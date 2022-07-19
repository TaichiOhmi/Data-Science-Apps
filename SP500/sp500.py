import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf

st.title('S&P 500 App')
st.markdown("""
S&P500の企業リストとそれに対応した株価終値（年間累計）を取得するアプリ
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")

st.sidebar.header('検索')

#スクレイピング
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/list_of_S%26P_500_companies'
    html = pd.read_html(url, header=0)
    df = html[0]
    return df
df = load_data()
sector = df.groupby('GICS Sector')

# サイドバー: セクター
sorted_sector_unique = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

# データフィルター
df_selected_sector = df[(df['GICS Sector'].isin(selected_sector))]

st.header('Results')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + '行 ' + str(df_selected_sector.shape[1]) + '列')
st.dataframe(df_selected_sector)

# データダウンロード
def file_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href
st.markdown(file_download(df_selected_sector), unsafe_allow_html=True)

# https://pypi.org/project/yfinance/

data = yf.download(
    tickers = list(df_selected_sector[:10].Symbol),
    period = "ytd",
    interval = "1d",
    group_by = "ticker",
    auto_adjust = True,
    prepost = True,
    threads = True,
    proxy = None
)

# Plot Closing Price of Query Symbol
def price_plot(symbol):
    df = pd.DataFrame(data[symbol].Close)
    df['Date'] = df.index
    plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
    plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing Price', fontweight='bold')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    return st.pyplot()

num_company = st.sidebar.slider('Number of Companies', 1, 5)

if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)