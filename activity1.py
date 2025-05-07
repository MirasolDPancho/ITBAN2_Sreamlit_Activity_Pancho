import streamlit as st
import pandas as pd

# Title
st.title("📁 CSV File Uploader & Filter")

# File upload
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Try reading the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

        st.subheader("📊 Preview of Uploaded Data")
        st.dataframe(df.head())

        # Show raw data toggle
        if st.sidebar.checkbox("Show full raw data"):
            st.write("🔍 Full Raw Data")
            st.dataframe(df)

        # Filter section
        st.sidebar.subheader("🔎 Filter Data")
        
        # Check if the DataFrame is empty
        if df.empty:
            st.warning("⚠️ The uploaded file is empty. Please upload a valid CSV file.")
        else:
            column_to_filter = st.sidebar.selectbox("Select a column", df.columns)

            unique_values = df[column_to_filter].dropna().unique()
            selected_values = st.sidebar.multiselect(f"Select value(s) for {column_to_filter}", unique_values)

            if selected_values:
                filtered_df = df[df[column_to_filter].isin(selected_values)]
                st.subheader(f"📂 Filtered Data based on {column_to_filter}")
                st.dataframe(filtered_df)

                # Download filtered data
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Filtered CSV",
                    data=csv,
                    file_name='filtered_data.csv',
                    mime='text/csv',
                )
            else:
                st.info("ℹ️ Please select at least one filter value from the sidebar.")

    except pd.errors.ParserError:
        st.error("❌ Error: The uploaded file is not a valid CSV file. Please upload a valid CSV file.")
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")

else:
    st.warning("⚠️ Please upload a CSV file to begin.")
