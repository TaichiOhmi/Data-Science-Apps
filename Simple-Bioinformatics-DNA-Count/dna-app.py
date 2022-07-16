from turtle import width
import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image

# header画像とタイトル
image = Image.open('dna-logo.jpeg') # 画像を読み込み
st.image(image, use_column_width=True) # 画像を表示

st.write("""
# DNA Nucleotide Count Web App

This app counts the nucleotide composition of query DNA!

###
""")

# インプットテキストボックス
st.sidebar.header('Enter DNA sequence')
st.header('Enter DNA sequence')

sequence_input = ">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

# text_areに表示。text_are('title?見出し?, 本文, 高さ')
sequence = st.text_area("Sequence input", sequence_input, height=200)
# sequenceを改行で区切ってリストに格納
sequence = sequence.splitlines()
# リストの最初の部分は必要ないので、スライスで省く
sequence = sequence[1:]
# リストの内容を結合
sequence = ''.join(sequence)

st.write("""
***
""")

## input DNA sequence を表示
st.header('INPUT (DNA QUERY)')
sequence

# DNA nucleotide count
st.header('OUTPUT (DNA Nucleotide Count)')

### Print dictionary
st.subheader('1. Print dictionary')
def DNA_nucleotide_count(seq):
    d = dict([
        ('A', seq.count('A')),
        ('T', seq.count('T')),
        ('G', seq.count('G')),
        ('C', seq.count('C')),
    ])
    return d

X = DNA_nucleotide_count(sequence)
X

X_label = list(X)
X_values = list(X.values())

# Print Text
st.subheader('2. Print text')
st.write('There are ' + str(X['A']) + ' adenine(A)')
st.write('There are ' + str(X['T']) + ' thymine(T)')
st.write('There are ' + str(X['G']) + ' guanine(G)')
st.write('There are ' + str(X['C']) + ' cytosine(C)')

# Display DataFrame
st.subheader('3. Display DataFrame')
df = pd.DataFrame.from_dict(X, orient='index')
df = df.rename({0:'count'}, axis='columns')
df.reset_index(inplace=True)
df = df.rename(columns={'index':'nucleotide'})
st.write(df)

# Display Bar Chart using Altair
st.subheader('4. Display Bar chart')
p = alt.Chart(df).mark_bar().encode(x='nucleotide', y='count')
p = p.properties(width=alt.Step(80))# 棒グラフの幅を調節
st.write(p)