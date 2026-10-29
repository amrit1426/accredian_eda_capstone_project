import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.set_page_config(page_title="Movie Revenue EDA", layout="wide")
st.title("🎬 Movie Revenue EDA Dashboard")
st.markdown("Exploratory analysis of movie revenue and ratings.")

df = pd.read_csv("20240715_CapstoneProject-1000movies_data.csv")

# Clean data similar to notebook: impute missing Revenue and Metascore with median
df["Revenue (Millions)"] = df["Revenue (Millions)"].fillna(df["Revenue (Millions)"].median())
df["Metascore"] = df["Metascore"].fillna(df["Metascore"].median())

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

# Yearly trends (notebook-derived)
st.subheader("Yearly Trends")
if len(filtered):
    yearly = filtered.groupby("Year").agg(
        Count=("Revenue (Millions)", "size"),
        MeanRevenue=("Revenue (Millions)", "mean"),
        SumRevenue=("Revenue (Millions)", "sum"),
    ).reset_index()

    c1, c2, c3 = st.columns(3)
    with c1:
        fig = px.line(yearly, x="Year", y="Count", title="Movies per Year")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.line(yearly, x="Year", y="MeanRevenue", title="Mean Revenue per Year (M)")
        st.plotly_chart(fig, use_container_width=True)
    with c3:
        fig = px.line(yearly, x="Year", y="SumRevenue", title="Total Revenue per Year (M)")
        st.plotly_chart(fig, use_container_width=True)

# Top movies
st.subheader("Top 10 Grossing Movies")
if len(filtered):
    top10 = (
        filtered.sort_values("Revenue (Millions)", ascending=False)
        .head(10)[["Title", "Director", "Year", "Revenue (Millions)", "Rating", "Metascore"]]
        .reset_index(drop=True)
    )
    st.dataframe(top10, use_container_width=True)

# Directors analysis
st.subheader("Top Directors")
if len(filtered):
    directors = filtered.groupby("Director").agg(
        Movies=("Revenue (Millions)", "size"),
        SumRevenue=("Revenue (Millions)", "sum"),
        MeanRevenue=("Revenue (Millions)", "mean"),
        AvgRating=("Rating", "mean"),
        AvgMetascore=("Metascore", "mean"),
    ).reset_index()

    top_by_revenue = directors.sort_values("SumRevenue", ascending=False).head(10)
    top_by_rating = directors.sort_values("AvgRating", ascending=False).head(10)
    top_by_metascore = directors.sort_values("AvgMetascore", ascending=False).head(10)

    d1, d2, d3 = st.columns(3)
    with d1:
        fig = px.bar(top_by_revenue, x="Director", y="SumRevenue", title="Total Revenue")
        fig.update_layout(xaxis_tickangle=-90)
        st.plotly_chart(fig, use_container_width=True)
    with d2:
        fig = px.bar(top_by_rating, x="Director", y="AvgRating", title="Avg Rating", color_discrete_sequence=["orange"])
        fig.update_layout(xaxis_tickangle=-90)
        st.plotly_chart(fig, use_container_width=True)
    with d3:
        fig = px.bar(top_by_metascore, x="Director", y="AvgMetascore", title="Avg Metascore", color_discrete_sequence=["blue"])
        fig.update_layout(xaxis_tickangle=-90)
        st.plotly_chart(fig, use_container_width=True)

# Correlations
st.subheader("Correlations with Revenue")
if len(filtered):
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=("Revenue vs Rating", "Revenue vs Metascore", "Revenue vs Votes", "Revenue vs Runtime"),
    )
    fig.add_trace(go.Scatter(x=filtered["Revenue (Millions)"], y=filtered["Rating"], mode="markers", name="Rating"), row=1, col=1)
    fig.add_trace(go.Scatter(x=filtered["Revenue (Millions)"], y=filtered["Metascore"], mode="markers", name="Metascore"), row=1, col=2)
    fig.add_trace(go.Scatter(x=filtered["Revenue (Millions)"], y=filtered["Votes"], mode="markers", name="Votes"), row=2, col=1)
    fig.add_trace(go.Scatter(x=filtered["Revenue (Millions)"], y=filtered["Runtime (Minutes)"], mode="markers", name="Runtime"), row=2, col=2)
    fig.update_layout(height=700, showlegend=False, title_text="Revenue vs Key Features")
    st.plotly_chart(fig, use_container_width=True)

# Genre combinations
st.subheader("Genre Combinations")
if len(filtered):
    gen_sum = (
        filtered.groupby("Genre")["Revenue (Millions)"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    gen_mean = (
        filtered.groupby("Genre")["Revenue (Millions)"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    g1, g2 = st.columns(2)
    with g1:
        fig = px.bar(gen_sum, x="Genre", y="Revenue (Millions)", title="Top Genres by Total Revenue")
        fig.update_layout(xaxis_tickangle=-90)
        st.plotly_chart(fig, use_container_width=True)
    with g2:
        fig = px.bar(gen_mean, x="Genre", y="Revenue (Millions)", title="Top Genres by Mean Revenue")
        fig.update_layout(xaxis_tickangle=-90)
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Data Preview")
st.dataframe(filtered.head(100))
