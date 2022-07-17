from enum import unique
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('NBA Player Stats')

st.markdown("""
NBAプレイヤーのスタッツを取得して表示するシンプルなアプリです。
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

# サイドバーで検索の詳細を受け取る
st.sidebar.header('検索')
# サイドバー：年
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2022))))

# スクレイピングとデータ処理
@st.cache
def load_data(year):
    url = 'https://www.basketball-reference.com//leagues/NBA_' + str(year) + '_per_game.html'
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selected_year)

# サイドバー：チーム
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)# 選択できる数を全てにしたいときは３つ目の引数にリスト全体を選択。他の数にしたい場合はスライスを使用する。(例: sorted_unique_team[:1]は１つまで。[:2]は２つまで、[:5]は５つまで。

# サイドバー：ポジション
# unique_position = ['C', 'PF', 'SF', 'PG', 'SG']
unique_position = list(playerstats.Pos.unique())
selected_pos = st.sidebar.multiselect('Position', unique_position, unique_position)

# データのフィルタリング
# playerstatsのTm(チーム)が選択したチームであり、Pos(ポジション)が選択したポジションの行だけ抜き出し、新たなDataFrameを作成
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))].astype(str)

# 結果の表示
st.header('Results')
st.write('データ構造：' + str(df_selected_team.shape[0]) + '行 ' + str(df_selected_team.shape[1]) + '列')
st.dataframe(df_selected_team)

# データのダウンロード
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href
st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('EDA-Basketball/output.csv', index=False)
    df = pd.read_csv('EDA-Basketball/output.csv')

    corr = df.corr()
    # np.zeros_like()で 値が0の行列を作り、np.triu_indices_from()で上三角形のインデックスを返し、そこを作成した０で埋めることで右半分を隠す
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style('white'):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(f)