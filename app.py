import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Page Config
st.set_page_config(page_title="Primetrade.ai Analytics", layout="wide")
st.title("📈 Trader Behavior vs Market Sentiment")

# 2. Load Data 
@st.cache_data
def load_data():
    # Load the core dataset we built in Part A
    df = pd.read_csv('merged_daily_trader_sentiment.csv')
    
    # Load the clusters we built in Bonus 1
    clusters = pd.read_csv('trader_clusters.csv')
    df = df.merge(clusters[['Account', 'Cluster']], on='Account', how='left')
    
    # Standardize names
    df['sentiment_group'] = df['classification'].replace({'Extreme Fear': 'Fear', 'Extreme Greed': 'Greed'})
    return df

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("Filter Dashboard")
sentiment_filter = st.sidebar.multiselect("Select Market Sentiment:", df['sentiment_group'].unique(), default=df['sentiment_group'].unique())
cluster_filter = st.sidebar.multiselect("Select Trader Archetype (Cluster):", df['Cluster'].dropna().unique(), default=df['Cluster'].dropna().unique())

filtered_df = df[(df['sentiment_group'].isin(sentiment_filter)) & (df['Cluster'].isin(cluster_filter))]

# 4. Top Level Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Avg Daily PnL", f"${filtered_df['daily_PnL'].mean():,.2f}")
col2.metric("Avg Win Rate", f"{filtered_df['win_rate'].mean():.1%}")
col3.metric("Avg Trade Size", f"${filtered_df['avg_trade_size_usd'].mean():,.2f}")

# 5. Visualizations
st.subheader("Performance Distributions")
fig, ax = plt.subplots(1, 2, figsize=(15, 5))

# Plot 1: PnL by Sentiment (Truncated outliers for readability)
sns.boxplot(data=filtered_df[filtered_df['daily_PnL'].abs() < 50000], x='sentiment_group', y='daily_PnL', ax=ax[0])
ax[0].set_title("Daily PnL Distribution by Market Sentiment")
ax[0].set_ylabel("Daily PnL (USD)")

# Plot 2: Trade Frequency by Archetype
sns.barplot(data=filtered_df, x='Cluster', y='num_trades', ax=ax[1])
ax[1].set_title("Average Daily Trade Frequency by Archetype")
ax[1].set_xlabel("Archetype Cluster (0=Whales, 1=HFT, 2=Shorts)")

st.pyplot(fig)
