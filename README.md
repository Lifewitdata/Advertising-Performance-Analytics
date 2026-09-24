<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&pause=1000&color=00D9FF&center=true&vCenter=true&width=650&lines=Advertising+Performance+Analytics;CTR+%C2%B7+CVR+%C2%B7+CPC+%C2%B7+CPA+Deep+Dive;Geo+%C2%B7+Device+%C2%B7+Campaign+%C2%B7+Audience+Insights;Built+with+Python+%2B+Pandas+%2B+Seaborn" alt="Typing SVG" />

<br/>

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Numerics-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-4CAF50?style=for-the-badge)

<br/>

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="500">

</div>

---

## 📌 Overview

**Advertising-Performance-Analytics** is an exploratory data analysis project that turns raw, daily advertising logs into decision-ready insight. It walks from messy CSV → clean dataframe → efficiency metrics → segmented visual stories, answering the question every media buyer actually asks:

> *"Where is our ad spend working — and where is it quietly leaking money?"*

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/216122041-518ac897-8d92-4c6b-9b3f-ca01dcaf38ee.png" width="500">
</div>

---

## 🎯 Objectives

- 🧹 Load, clean, and validate daily advertising data
- 📐 Calculate core efficiency metrics — **CTR, CVR, CPC, CPA**
- 🌍 Compare performance across **geo** and **device**
- 🏆 Identify high-performing **campaigns** and **audience segments**
- 📈 Visualize trends to support faster, sharper decision-making

---

## 📂 Dataset

<div align="center">

| Column | Description |
|---|---|
| `event_date` | Date of the recorded activity |
| `geo` | Geographic market |
| `device` | Device type (mobile / desktop / tablet) |
| `campaign_id` | Unique campaign identifier |
| `audience_id` | Audience segment identifier |
| `impressions` | Ad views served |
| `clicks` | Ad clicks recorded |
| `conversions` | Completed conversion events |
| `cost` | Total spend |

</div>

**Source file:** [`ads_daily_preview.csv`](./ads_daily_preview.csv) — daily aggregated advertising metrics.

---

## 🛠️ Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/-Python-05122A?style=flat&logo=python)
![Pandas](https://img.shields.io/badge/-Pandas-05122A?style=flat&logo=pandas)
![NumPy](https://img.shields.io/badge/-NumPy-05122A?style=flat&logo=numpy)
![Matplotlib](https://img.shields.io/badge/-Matplotlib-05122A?style=flat&logo=plotly)
![Seaborn](https://img.shields.io/badge/-Seaborn-05122A?style=flat&logo=seaborn)
![Jupyter](https://img.shields.io/badge/-Jupyter-05122A?style=flat&logo=jupyter)

</div>

---

## 📊 Key Metrics Explained

| Metric | Formula | What it tells you |
|---|---|---|
| **CTR** | clicks ÷ impressions | Ad relevance & creative appeal |
| **CVR** | conversions ÷ clicks | Landing page & offer effectiveness |
| **CPC** | cost ÷ clicks | Efficiency of paid traffic acquisition |
| **CPA** | cost ÷ conversions | True cost of a customer outcome |

---

## 🚀 Getting Started

```bash
# Clone the repo
git clone https://github.com/Lifewitdata/Advertising-Performance-Analytics.git
cd Advertising-Performance-Analytics

# Install dependencies
pip install pandas numpy matplotlib seaborn jupyter

# Launch the notebook
jupyter notebook "Advertising Performance Analytics.ipynb"
```

---

## 🗺️ Workflow

```mermaid
flowchart LR
    A[📥 Raw CSV] --> B[🧹 Clean & Validate]
    B --> C[📐 Compute CTR / CVR / CPC / CPA]
    C --> D[🌍 Segment by Geo & Device]
    D --> E[🏆 Rank Campaigns & Audiences]
    E --> F[📈 Visualize & Report Insights]
```

---

## 💡 Sample Insight Style

> Each chart in the notebook closes with a written takeaway, e.g.:
> *"Mobile CTR outpaces desktop by 1.4x in APAC, but desktop converts at nearly 2x the rate — spend allocation should reflect that split rather than a flat device budget."*

---

<div align="center">

### ⭐ If this project helped you think about ad analytics differently, consider starring it!

<img src="https://user-images.githubusercontent.com/74038190/212284158-e840e285-664b-44d7-b79b-e264b5e54825.gif" width="100%">

</div>
