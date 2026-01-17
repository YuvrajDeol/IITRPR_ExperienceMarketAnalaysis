# AI Experience Market Planner (Concert • Standup • Workshop)

An AI-based planner that analyzes **historical demand signals** for experience markets and generates recommendations on:
- **What type of show to run** (Concert / Standup / Workshop)
- **Which city to target**
- **Which month to schedule**
- **Whether to increase / decrease price, keep price, or pause**

The dashboard is built using **Streamlit** and uses **Google Trends + Seasonality** along with a **city payment power multiplier** to simulate city-level purchasing strength.

---

## Problem Statement
Experience-based businesses often struggle to decide the **right event category**, **right city**, and **optimal ticket pricing**. Decisions are frequently based on intuition, which can lead to poor turnout or incorrect pricing.

This project creates an **AI Experience Market Planner** that uses trend analytics and seasonal patterns to generate actionable planning recommendations.

---

## Approach / Architecture
### Data Sources
- **Google Trends CSV files** (`multiTimeline (1).csv` to `multiTimeline (35).csv`)
- **Seasonality dataset** (`Seasonality.csv`)
- **City payment power multiplier** (heuristic-based adjustment)

### Processing Pipeline
1. Load all Google Trends CSVs and convert them into a single long-format dataset
2. Extract `Month` and `Year` from dates
3. Merge with seasonality weights by month
4. Compute a combined `Demand_Index` using:
   - Trend interest score
   - Seasonality score (scaled)
5. Map keywords into 3 categories:
   - Concert
   - Standup
   - Workshop
6. Apply city multiplier and generate pricing recommendations
7. Display results in an interactive Streamlit dashboard

---

## Core Features
- **Show Type Selection** (Concert / Standup / Workshop)
- **City Selection** (dropdown with spending-power multiplier)
- **Month Selection**
- **Ticket Price Slider**
- **Demand Snapshot**
  - Avg Demand Index
  - City multiplier
  - Adjusted demand
- **Recommended Ticket Price**
- **Action Recommendation**
  - INCREASE PRICE
  - DECREASE PRICE
  - KEEP
  - REMOVE / PAUSE
- **Planner Table**
  - Add recommendations to a plan
  - Export plan as CSV

---

## Tech Stack
- **Python**
- **Pandas** (data cleaning + aggregation)
- **Streamlit** (dashboard)
- **Requests** (fetch CSVs from GitHub)
- **Cloudflared** (public URL tunnel for Colab demo)

---

## How to Run (Locally)
### 1) Install dependencies
```bash
pip install -r requirements.txt
