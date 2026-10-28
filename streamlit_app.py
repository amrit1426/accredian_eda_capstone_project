import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Movie Revenue EDA", layout="wide")
st.title("🎬 Movie Revenue EDA Dashboard")
st.markdown("Exploratory analysis of movie revenue and ratings.")

df = pd.read_csv("20240715_CapstoneProject-1000movies_data.csv")

with st.sidebar:
    st.header("Filters")
    genres = st.multiselect("Genre", options=df["genre"].dropna().unique(), default=df["genre"].dropna().unique())
    year_range = st.slider("Release Year", int(df["year"].min()), int(df["year"].max()), (int(df["year"].min()), int(df["year"].max())))

filtered = df[
    df["genre"].isin(genres) &
    df["year"].between(year_range[0], year_range[1])
]

col1, col2, col3 = st.columns(3)
col1.metric("Movies", len(filtered))
col2.metric("Avg Revenue (M)", f"{filtered['revenue'].mean():.2f}" if len(filtered) else "N/A")
col3.metric("Avg Rating", f"{filtered['rating'].mean():.1f}" if len(filtered) else "N/A")

st.subheader("Revenue by Genre")
if len(filtered):
    fig = px.bar(filtered.groupby("genre")["revenue"].mean().reset_index(), x="genre", y="revenue")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Rating vs Revenue")
if len(filtered):
    fig = px.scatter(filtered, x="rating", y="revenue", color="genre", hover_data=["name"])
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Movies per Year")
if len(filtered):
    fig = px.histogram(filtered, x="year", nbins=30)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Data Preview")
st.dataframe(filtered.head(100))
