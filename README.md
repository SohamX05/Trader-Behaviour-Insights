# Trader Behavior vs Market Sentiment

This repository contains my analysis of Hyperliquid trader performance against the Bitcoin Fear & Greed Index. 

## Project Structure
* `analysis.ipynb`: The core Jupyter Notebook containing data preparation, segmentation analysis, and machine learning bonuses.
* `app.py`: An interactive Streamlit dashboard summarizing the insights.
* `merged_daily_trader_sentiment.csv`: The cleaned, aligned dataset at the daily/account level.
* `trader_clusters.csv`: Account mappings to K-Means behavioral archetypes.

---

## Part A: Methodology & Data Preparation
* **Data Cleansing:** The Hyperliquid trader dataset (211,224 rows) and the Fear/Greed index (2,644 rows) were analyzed. No nulls or duplicates were found in either file.
* **Alignment:** Extracted the standard Date from `Timestamp IST` and matched it against the sentiment dataset.
* **Feature Engineering:** Aggregated individual trades up to an Account-Daily level to calculate `daily_PnL`, `win_rate`, `avg_trade_size`, `num_trades`, and `long_ratio`. Classifications were simplified (combining Extreme Fear/Greed into Fear/Greed).

---

## Part B: Key Insights & Evidence

**1. Market "Fear" drives higher PnL but slightly lower hit rates.**
Contrary to the belief that panic ruins performance, data shows average daily PnL is highest during **Fear ($5,185)** compared to **Greed ($4,144)**. However, the win rate is slightly *lower* during Fear (84.2%) vs Greed (85.6%). Traders make fewer winning trades, but their winning magnitudes are larger due to volatility.

**2. Trader behavior drastically shifts into high gear during Fear.**
Traders become highly active and aggressive when the market panics:
* **Frequency:** Trades per day jump from 77 (Greed) to 105 (Fear).
* **Size:** Average trade sizes balloon from $5,954 (Greed) to $8,529 (Fear).
* **Bias:** Traders exhibit a "buy the dip" bias. The Long/Short ratio tilts to 52.1% Long during Fear, compared to just 47.2% during Greed.

**3. Segmentation: Frequent vs. Infrequent Traders.**
When segmenting by median daily trade frequency:
* **Frequent Traders** thrive during Fear, banking an average of **$9,391 PnL/day**. 
* **Infrequent Traders** perform terribly during Fear, generating only **$848 PnL/day**, despite pushing their average trade size up to an aggressive $11,223. They perform much better during Greed days ($1,497 PnL/day) when trends are smoother.

---

## Part C: Actionable Output (Strategy Rules)

Based on these quantitative insights, here are two actionable trading rules:

* **Rule 1 (Capital Allocation):** *Scale up capital allocation for High-Frequency accounts during "Fear" markets.* The data conclusively shows that frequent traders thrive on the volatility of Fear days, capturing roughly 36% more PnL than they do on Greed days.
* **Rule 2 (Risk Management):** *Restrict trade size limits on "Infrequent/Discretionary" traders during Fear markets.* Currently, infrequent traders dangerously double their average trade sizes to ~$11,223 during panics, yet their PnL crashes. Restrict their size during Fear, and encourage them to scale up during "Greed" when their hit rate naturally peaks.

---

## Bonus Delivered 🚀

1. **Behavioral Clustering:** Used K-Means to segment accounts into 3 archetypes: *Whales* (Massive size, low frequency), *HFT Algos* (Massive frequency, low size), and *Short-Sellers* (Low win-rate, high short-bias). 
2. **Predictive ML Model:** Built a Random Forest model capable of predicting if a trader will be profitable *tomorrow* with **68% accuracy**. Surprisingly, today's Win Rate is a far better predictor of tomorrow's PnL than the actual Market Sentiment score.
3. **Interactive Dashboard:** Run the following command in your terminal to explore the segmented charts interactively:
   ```bash
   streamlit run app.py
