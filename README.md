# Automated Equity Research & Valuation Dashboard
### *An End-to-End Financial Engineering & Decision Support Suite*

## 📌 Project Overview
This project automates the complex process of fundamental equity valuation. By bridging the gap between raw market data and actionable insights, it allows users to determine the **Intrinsic Value** of a company using an automated **Three-Stage Discounted Cash Flow (DCF)** model.

The goal is to provide a "grounded" alternative to market price by calculating a stock's fair value based on future cash flows rather than short-term sentiment. This tool filters out market noise to highlight stocks trading at a significant margin of safety.

## ⚖️ Model Logic: Stage 1 vs. Stage 2 vs. Stage 3
To provide a more realistic valuation, this pipeline avoids the common mistake of "growth cliffs" by implementing a transitionary fading logic.

| Feature | Stage 1: High Growth | Stage 2: Linear Fade | Stage 3: Terminal Stability |
| :--- | :--- | :--- | :--- |
| **Timeframe** | Years 1 - 5 | Years 6 - 10 | Years 11 - 20+ |
| **Growth Logic** | User-defined conviction ($G1$). | **Linear Step-Down** calculation. | Mature $G3$ capped at economic growth. |
| **Market Context** | Peak competitive advantage. | Competitive convergence/saturation. | Long-term GDP alignment. |
| **Valuation Aim** | Capture near-term alpha. | Smooth transition to maturity. | Sustainable perpetual value. |

## 🚀 Key Features
* **Three-Stage Growth Logic:** Uses a custom Python algorithm to calculate an annual step-down in growth rates during Stage 2, simulating natural business maturation.
* **Hybrid Terminal Value:** Average of two professional methodologies—**Gordon Growth** and **Exit Multiples** (capped at 15-20x)—to prevent over-sensitivity to terminal assumptions.
* **Automated Data Pipeline:** Integration with `yfinance` to scrape real-time Operating Cash Flow, CapEx, Total Cash, and Total Debt.
* **Dynamic WACC Calculation:** Automatically adjusts the discount rate based on a stock’s specific **Beta**, ensuring the valuation is risk-adjusted.
* **Interactive "What-If" Analysis:** Built-in feedback loop where changes in the Excel "Control Center" instantly update the Power BI visuals upon refresh.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Libraries:** Pandas, yfinance, NumPy
* **Visualization:** Power BI
* **Configuration:** Microsoft Excel

## 📊 Dashboard Visuals
<img width="1266" height="722" alt="image" src="https://github.com/user-attachments/assets/19242558-001a-4f83-bdd9-a9328d1cec6e" />
The pipeline generates structured data optimized for the following Power BI visuals:

* **Intrinsic vs. Market PX (Scatter Plot):** Maps risk vs. reward; tickers below the diagonal line represent "under-priced" opportunities.
* **Equity Valuation Upside (Bar Chart):** A ranked leaderboard of stocks by upside percentage, utilizing conditional formatting to highlight the margin of safety (e.g., strong buy vs overvalued).
* **Key Performance Indicators (KPI Cards):** Real-time summary metrics for aggregate portfolio health, including **Avg Upside %** and **Total Intrinsic Value**.
* **Ticker Slicer & Assumption Table:** Interactive components allowing for easy stock filtering and quick reference to user-defined growth rate inputs.

## ⚙️ Setup Instructions
1.  **Clone the Repository:** Download the `.pbix` and `tickers_config.xlsx` files.
2.  **Define Assumptions:** Open the Excel file and enter your $G1, G2,$ and $G3$ growth expectations for your target tickers.
3.  **Configure Power BI Path:**
    * Open the `.pbix` file.
    * Navigate to **Transform Data > Source (Python Script)**.
    * Update the file path variable to match the location of `tickers_config.xlsx` on your machine.
4.  **Execute & Refresh:** Click **Refresh** in the Power BI ribbon. The Python engine will fetch live data, apply your fade logic, and update the interactive dashboard.
