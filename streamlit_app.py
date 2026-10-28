import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Movie Revenue EDA", layout="wide")
st.title("🎬 Movie Revenue EDA Dashboard")
st.markdown("Exploratory analysis of movie revenue and ratings.")

df = pd.read_csv("20240715_CapstoneProject-1000movies_data.csv")

with st.sidebar:
    st.header("Filters")
    genres = st.multiselect("Genre", options=df["Genre"].dropna().unique(), default=df["Genre"].dropna().unique())
    year_range = st.slider("Release Year", int(df["Year"].min()), int(df["Year"].max()), (int(df["Year"].min()), int(df["Year"].max())))

filtered = df[
    df["Genre"].isin(genres) &
    df["Year"].between(year_range[0], year_range[1])
]

col1, col2, col3 = st.columns(3)
col1.metric("Movies", len(filtered))
col2.metric("Avg Revenue (M)", f"{filtered['Revenue (Millions)'].mean():.2f}" if len(filtered) else "N/A")
col3.metric("Avg Rating", f"{filtered['Rating'].mean():.1f}" if len(filtered) else "N/A")

st.subheader("Revenue by Genre")
if len(filtered):
    fig = px.bar(filtered.groupby("Genre")["Revenue (Millions)"].mean().reset_index(), x="Genre", y="Revenue (Millions)")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Rating vs Revenue")
if len(filtered):
    fig = px.scatter(filtered, x="Rating", y="Revenue (Millions)", color="Genre", hover_data=["Title"])
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Movies per Year")
if len(filtered):
    fig = px.histogram(filtered, x="Year", nbins=30)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Data Preview")
st.dataframe(filtered.head(100))
