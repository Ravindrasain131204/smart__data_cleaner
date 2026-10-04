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
        st.subheader("Clean your data")

    remove_dupes = st.checkbox("Remove duplicate rows")
    missing_option = st.selectbox(
        "How to handle missing values?",
        ["Do nothing", "Drop rows with missing values", "Fill missing values (numbers = mean, text = Unknown)"]
    )

    clean_df = df.copy()

    if remove_dupes:
        clean_df = clean_df.drop_duplicates()

    if missing_option == "Drop rows with missing values":
        clean_df = clean_df.dropna()
    elif missing_option == "Fill missing values (numbers = mean, text = Unknown)":
        num_cols = clean_df.select_dtypes(include="number").columns
        text_cols = clean_df.select_dtypes(exclude="number").columns
        clean_df[num_cols] = clean_df[num_cols].fillna(clean_df[num_cols].mean())
        clean_df[text_cols] = clean_df[text_cols].fillna("Unknown")

    st.subheader("Cleaned data")
    st.dataframe(clean_df.head(10))
    st.write("Rows before:", df.shape[0], "| Rows after:", clean_df.shape[0])

    csv = clean_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download cleaned CSV", csv, "cleaned_data.csv", "text/csv")