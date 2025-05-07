import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")
st.title("🦠 COVID-19 Data Dashboard")

# Sidebar for country selection
st.sidebar.title("🌍 Country Selector")
country_list_url = "https://disease.sh/v3/covid-19/countries"
response = requests.get(country_list_url)
country_data = response.json()
countries = [country['country'] for country in country_data]

country = st.sidebar.selectbox("Choose a country", countries)

# Fetch historical data
url = f"https://disease.sh/v3/covid-19/historical/{country}?lastdays=30"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    if "timeline" in data:
        timeline = data["timeline"]
        df = pd.DataFrame({
            "Date": pd.to_datetime(list(timeline["cases"].keys())),
            "Cases": list(timeline["cases"].values()),
            "Deaths": list(timeline["deaths"].values()),
            "Recovered": list(timeline["recovered"].values()),
        })

        # Compute daily differences
        df["New Cases"] = df["Cases"].diff().fillna(0)
        df["New Deaths"] = df["Deaths"].diff().fillna(0)
        df["New Recovered"] = df["Recovered"].diff().fillna(0)

        st.subheader(f"📊 Daily Statistics for {country}")

        col1, col2, col3 = st.columns(3)
        col1.metric("New Cases (Latest)", int(df['New Cases'].iloc[-1]))
        col2.metric("New Deaths (Latest)", int(df['New Deaths'].iloc[-1]))
        col3.metric("New Recovered (Latest)", int(df['New Recovered'].iloc[-1]))

        # 1. Line Chart: New Cases, Deaths, and Recovered
        st.subheader("📈 Daily New Cases, Deaths, and Recovered")
        st.line_chart(df.set_index("Date")[["New Cases", "New Deaths", "New Recovered"]])

        # 2. Pie Chart: Proportion of Total
        st.subheader("📊 Proportion of Total Cases, Deaths, and Recovered")
        totals = {
            "Cases": df["Cases"].iloc[-1],
            "Deaths": df["Deaths"].iloc[-1],
            "Recovered": df["Recovered"].iloc[-1],
        }
        fig1, ax1 = plt.subplots()
        ax1.pie(totals.values(), labels=totals.keys(), autopct="%1.1f%%", startangle=90)
        ax1.axis("equal")
        st.pyplot(fig1)

        # 3. Bar Chart: Cumulative Cases, Deaths, and Recovered over Time
        st.subheader("📊 Cumulative Cases, Deaths, and Recovered Over Time")
        df_cumulative = df[["Date", "Cases", "Deaths", "Recovered"]].set_index("Date")
        df_cumulative.plot(kind="bar", stacked=True, figsize=(10, 6), color=["blue", "red", "green"])
        plt.title("Cumulative Cases, Deaths, and Recovered")
        plt.xlabel("Date")
        plt.ylabel("Count")
        st.pyplot(plt)

        # 4. Bar Chart: Daily New Cases, Deaths, and Recovered
        st.subheader("📊 Daily New Cases, Deaths, and Recovered Comparison")
        df_daily = df[["Date", "New Cases", "New Deaths", "New Recovered"]].set_index("Date")
        df_daily.plot(kind="bar", stacked=True, figsize=(10, 6), color=["blue", "red", "green"])
        plt.title("Daily New Cases, Deaths, and Recovered")
        plt.xlabel("Date")
        plt.ylabel("Count")
        st.pyplot(plt)

        # 5. Area Chart: Cumulative Trend of Cases, Deaths, and Recovered
        st.subheader("📊 Cumulative Trend of Cases, Deaths, and Recovered")
        df_area = df[["Date", "Cases", "Deaths", "Recovered"]].set_index("Date")
        df_area.plot(kind="area", figsize=(10, 6), alpha=0.5, color=["blue", "red", "green"])
        plt.title("Cumulative Trend of Cases, Deaths, and Recovered")
        plt.xlabel("Date")
        plt.ylabel("Count")
        st.pyplot(plt)

        # Toggle for raw data
        if st.sidebar.checkbox("Show Raw Data"):
            st.subheader("🗃 Raw Data Table")
            st.dataframe(df)

        # Option to download data
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Raw Data",
            data=csv,
            file_name=f"{country}_covid_data.csv",
            mime='text/csv',
        )
    else:
        st.error("⚠️ Timeline data not found for this country.")
else:
    st.error(f"❌ API error: {response.status_code}")
