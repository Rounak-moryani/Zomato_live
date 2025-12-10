import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Zomato Restaurant Explorer",
    layout="wide",
    page_icon="🍽️"
)

# -----------------------------
# Custom Dark Theme CSS
# -----------------------------
st.markdown("""
    <style>
        body, .stApp {
            background-color: #0e1117 !important;
            color: #fafafa !important;
        }
        .css-1d391kg, .css-q8sbsg {
            background-color: #161a22 !important;
        }
        .stSelectbox div div {
            color: #ffffff !important;
        }
        .block-container {
            padding-top: 20px;
        }
        h1, .stMarkdown, .stWrite, .stSubheader {
            color: #ffffff !important;
        }
        .stDataFrame {
            background-color: #1b1e27 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align:center;'>🍽️ Zomato Restaurant Analysis</h1>", unsafe_allow_html=True)
st.write("Explore top-rated restaurants in your favorite location with cost comparison and interactive insights.")

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
selected_location = st.selectbox("📍 Select Location:", locations)

# Filter dataset
lo = df[df["location"] == selected_location]

if lo.empty:
    st.warning("⚠️ No restaurants found for this location.")
else:
    st.subheader(f"⭐ Top 10 Restaurants by Rating in **{selected_location}**")

    d = (
        lo.groupby("name")[["approx_cost", "rate"]]
        .mean()
        .nlargest(10, "rate")
        .reset_index()
    )

    col1, col2 = st.columns(2)

    # -----------------------------
    # Cost Comparison Chart
    # -----------------------------
    with col1:
        st.write("### 💰 Average Cost")
        fig_cost = px.bar(
            d, x="name", y="approx_cost",
            template="plotly_dark",
            title="Cost Comparison",
            hover_name="name"
        )
        fig_cost.update_layout(xaxis_tickangle=35, height=450)
        st.plotly_chart(fig_cost, use_container_width=True)

    # -----------------------------
    # Ratings Chart
    # -----------------------------
    with col2:
        st.write("### ⭐ Average Rating")
        fig_rate = px.bar(
            d, x="name", y="rate",
            template="plotly_dark",
            title="Rating Comparison",
            hover_name="name",
            color="rate",
            color_continuous_scale="reds"
        )
        fig_rate.update_layout(xaxis_tickangle=35, height=450)
        st.plotly_chart(fig_rate, use_container_width=True)

    # Show data table
    st.write("### 📋 Top Restaurants Data")
    st.dataframe(d.style.highlight_max(subset=["rate"], color="green"))


# Footer
st.markdown("<p style='text-align:center; color:gray;'>Made with ❤️ using Streamlit</p>", unsafe_allow_html=True)
