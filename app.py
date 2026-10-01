# import streamlit as st
# st.title ("Smart Data Cleaner")
# # st.write("HEllo! Upload a messy file and  i'll clean it")

import streamlit as st
import pandas as pd

st.title("Smart Data Cleaner")

file = st.file_uploader("Upload a CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    st.subheader("Preview of your data")
    st.dataframe(df.head(10))
    st.write("Rows:", df.shape[0], "| Columns:", df.shape[1])