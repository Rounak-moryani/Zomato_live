import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Zomato Restaurant Explorer", layout="wide")

st.title("🍽️ Zomato Restaurant Analysis")
st.write("Explore top-rated restaurants in each location.")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Zomato_Live.csv")
    df = df.drop(columns=['Unnamed: 0'], errors='ignore')
    return df

df = load_data()

# -----------------------------
# Location Selector
# -----------------------------
locations = sorted(df.location.dropna().unique())

selected_location = st.selectbox("Select a location:", locations)

# Filter data by selected location
lo = df[df["location"] == selected_location]

if lo.empty:
    st.warning("No restaurants found for this location.")
else:
    # -----------------------------
    # Compute Top Restaurants
    # -----------------------------
    d = (
        lo.groupby("name")[["approx_cost", "rate"]]
        .mean()
        .nlargest(10, "rate")
        .reset_index()
    )

    st.subheader(f"⭐ Top 10 Restaurants by Rating in {selected_location}")

    # -----------------------------
    # Plot 1 – Cost
    # -----------------------------
    st.write("### 💰 Approx Cost Comparison")

    fig1 = plt.figure(figsize=(16, 6))
    sb.barplot(x=d.name, y=d.approx_cost, palette="winter")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig1)

    # -----------------------------
    # Plot 2 – Ratings
    # -----------------------------
    st.write("### ⭐ Average Rating Comparison")

    fig2 = plt.figure(figsize=(16, 6))
    sb.barplot(x=d.name, y=d.rate, palette="hot")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig2)

    # Show table
    st.write("### 📋 Top 10 Restaurants Data")
    st.dataframe(d)
