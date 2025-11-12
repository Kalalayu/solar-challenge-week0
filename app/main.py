import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# 1. Set data directory
DATA_DIR = Path(r"C:\Users\Dell\Pictures\Solar-challenge-week0\Solar-challenge-week0\data")

# 2. Let user select multiple countries
countries = ["Benin", "Togo", "Sierra Leone"]
selected_countries = st.multiselect("Select countries to compare:", countries, default=countries)

if selected_countries:
    # 3. Load CSVs for selected countries and combine them
    file_map = {
        "Benin": DATA_DIR / "benin-clean.csv",
        "Togo": DATA_DIR / "togo-clean.csv",
        "Sierra Leone": DATA_DIR / "sierraleone-clean.csv"
    }

    combined_df = pd.DataFrame()
    for country in selected_countries:
        df = pd.read_csv(file_map[country])
        df["Country"] = country  # Add a column to identify the country
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    st.write("### Combined Solar Dataset")
    st.dataframe(combined_df.head())

    # Define colors for countries
    colors = sns.color_palette("tab10", n_colors=len(selected_countries))
    color_map = dict(zip(selected_countries, colors))

    # 4. Boxplot for GHI
    st.write("#### GHI Comparison Boxplot")
    fig, ax = plt.subplots()
    data_to_plot = [combined_df[combined_df["Country"] == c]["GHI"].dropna() for c in selected_countries]
    bplot = ax.boxplot(data_to_plot, labels=selected_countries, patch_artist=True)
    for patch, country in zip(bplot['boxes'], selected_countries):
        patch.set_facecolor(color_map[country])
    ax.set_ylabel("GHI")
    st.pyplot(fig)

    # 5. Line plot: Average daily GHI per country (if 'Date' column exists)
    if "Date" in combined_df.columns:
        st.write("#### Average Daily GHI")
        fig, ax = plt.subplots()
        for country in selected_countries:
            df_country = combined_df[combined_df["Country"] == country].copy()
            df_country["Date"] = pd.to_datetime(df_country["Date"], errors='coerce')
            df_country = df_country.dropna(subset=["Date"])
            if not df_country.empty:
                daily_avg = df_country.groupby("Date")["GHI"].mean()
                ax.plot(daily_avg.index, daily_avg.values, label=country, color=color_map[country])
        ax.set_ylabel("Average GHI")
        ax.set_xlabel("Date")
        ax.legend()
        st.pyplot(fig)
    else:
        st.write("No 'Date' column found. Line plot cannot be displayed.")

    # 6. Histogram for GHI distribution
    st.write("#### GHI Distribution")
    fig, ax = plt.subplots()
    for country in selected_countries:
        sns.histplot(
            combined_df[combined_df["Country"] == country]["GHI"].dropna(),
            label=country,
            kde=True,
            ax=ax,
            color=color_map[country],
            alpha=0.5
        )
    ax.set_xlabel("GHI")
    ax.set_ylabel("Frequency")
    ax.legend()
    st.pyplot(fig)

    # 7. Scatter plot: GHI vs Temperature (if 'Temperature' column exists)
    if "Temperature" in combined_df.columns:
        st.write("#### GHI vs Temperature Scatter Plot")
        fig, ax = plt.subplots()
        for country in selected_countries:
            df_country = combined_df[combined_df["Country"] == country]
            ax.scatter(
                df_country["Temperature"], 
                df_country["GHI"], 
                label=country, 
                color=color_map[country],
                alpha=0.6
            )
        ax.set_xlabel("Temperature")
        ax.set_ylabel("GHI")
        ax.legend()
        st.pyplot(fig)
else:
    st.write("Please select at least one country to compare.")
