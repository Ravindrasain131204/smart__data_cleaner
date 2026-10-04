import streamlit as st
import pandas as pd

st.title("Smart Data Cleaner")

file = st.file_uploader("Upload a CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    st.subheader("Preview of your data")
    st.dataframe(df.head(10))
    st.write("Rows:", df.shape[0], "| Columns:", df.shape[1])
    
    
    st.subheader("Data quality check")

    missing = df.isnull().sum()
    missing = missing[missing > 0]
    duplicates = df.duplicated().sum()

    col1, col2 = st.columns(2)
    col1.metric("Duplicate rows", duplicates)
    col2.metric("Columns with missing values", len(missing))

    if len(missing) > 0:
        st.write("Missing values per column:")
        st.dataframe(missing.rename("Missing count"))
    else:
        st.success("No missing values found!")