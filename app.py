# ---------- Imports ----------
import streamlit as st          # builds the web app
import pandas as pd             # handles the data
import plotly.express as px     # makes the charts

# ---------- Page title ----------
st.title("Smart Data Cleaner")

# ---------- Step 1: Upload ----------
# Shows an upload box in the browser; only accepts CSV files
file = st.file_uploader("Upload a CSV file", type=["csv"])

# Everything below runs only after a file is uploaded
if file is not None:
    df = pd.read_csv(file)      # read the CSV into a DataFrame

    # ---------- Step 2: Preview ----------
    st.subheader("Preview of your data")
    st.dataframe(df.head(10))   # show the first 10 rows
    st.write("Rows:", df.shape[0], "| Columns:", df.shape[1])

    # ---------- Step 3: Data quality check ----------
    st.subheader("Data quality check")

    missing = df.isnull().sum()         # count empty cells in each column
    missing = missing[missing > 0]      # keep only columns that have missing values
    duplicates = df.duplicated().sum()  # count repeated rows

    # Show the two numbers side by side
    col1, col2 = st.columns(2)
    col1.metric("Duplicate rows", duplicates)
    col2.metric("Columns with missing values", len(missing))

    # Show which columns have missing values (or a success message)
    if len(missing) > 0:
        st.write("Missing values per column:")
        st.dataframe(missing.rename("Missing count"))
    else:
        st.success("No missing values found!")

    # ---------- Step 4: Cleaning options ----------
    st.subheader("Clean your data")

    # Checkbox: user decides whether to remove duplicates
    remove_dupes = st.checkbox("Remove duplicate rows")

    # Dropdown: user decides how to handle missing values
    missing_option = st.selectbox(
        "How to handle missing values?",
        ["Do nothing", "Drop rows with missing values", "Fill missing values (numbers = mean, text = Unknown)"]
    )

    clean_df = df.copy()    # work on a copy so the original data stays safe

    # Apply: remove duplicate rows
    if remove_dupes:
        clean_df = clean_df.drop_duplicates()

    # Apply: handle missing values
    if missing_option == "Drop rows with missing values":
        clean_df = clean_df.dropna()    # delete rows that have any empty cell
    elif missing_option == "Fill missing values (numbers = mean, text = Unknown)":
        num_cols = clean_df.select_dtypes(include="number").columns     # number columns
        text_cols = clean_df.select_dtypes(exclude="number").columns    # text columns
        clean_df[num_cols] = clean_df[num_cols].fillna(clean_df[num_cols].mean())  # fill numbers with the average
        clean_df[text_cols] = clean_df[text_cols].fillna("Unknown")                # fill text with "Unknown"

    # ---------- Step 5: Show cleaned result ----------
    st.subheader("Cleaned data")
    st.dataframe(clean_df.head(10))
    st.write("Rows before:", df.shape[0], "| Rows after:", clean_df.shape[0])

    # ---------- Step 6: Download ----------
    csv = clean_df.to_csv(index=False).encode("utf-8")   # convert cleaned data to CSV bytes
    st.download_button("Download cleaned CSV", csv, "cleaned_data.csv", "text/csv")

    # ---------- Step 7: Charts ----------
    st.subheader("Visual summary")

    # Bar chart: missing values per column (only if there are any)
    if len(missing) > 0:
        missing_df = missing.reset_index()
        missing_df.columns = ["Column", "Missing count"]    # name the columns clearly
        fig1 = px.bar(
            missing_df,
            x="Column",
            y="Missing count",
            title="Missing values per column (original data)"
        )
        st.plotly_chart(fig1)

    # Histogram: distribution of any numeric column the user picks
    numeric_cols = clean_df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        chosen = st.selectbox("Pick a column to see its distribution", numeric_cols)
        fig2 = px.histogram(clean_df, x=chosen, title=f"Distribution of {chosen}")
        st.plotly_chart(fig2)