📊 Interactive Visualization & Dashboarding
The Power BI front-end transforms complex Python outputs into an "at-a-glance" executive dashboard.

1. Visual Hierarchy & Insights
Intrinsic vs. Market Price (Scatter Plot): This visual maps risk versus reward. Tickers above the diagonal "Fair Value" line represent potential overvaluations, while those below are identified as "under-priced" opportunities.

Equity Valuation Upside (Bar Chart): Provides a ranked leaderboard of the most attractive investment opportunities based on the calculated margin of safety.

Key Performance Indicators (KPI Cards): Display aggregate portfolio health, including average upside percentage and total market capitalization coverage.

2. The Integrated Workflow (Excel + Power BI)
The system is designed to be a "living model" where the user acts as the Chief Investment Officer:

The "Control Center" (Excel): Users define their own conviction levels by adjusting G1-G3 growth rates in tickers_config.xlsx. This allows for instant "what-if" scenario analysis.

The "Engine" (Python): Upon clicking Refresh in Power BI, the Python script triggers, pulling the new Excel assumptions and merging them with live market data from the Yahoo Finance API.

The "Front-End" (Power BI): The dashboard automatically re-calculates all DCF models and updates the charts, providing a real-time feedback loop between user assumptions and market reality.

📉 Valuation Methodology
The core of this project is a Three-Stage Discounted Cash Flow (DCF) model that automates the transition from high-growth phases to terminal stability.

1. Three-Stage Growth Logic
To avoid "growth cliffs" and unrealistic valuations, the Python script implements three distinct phases:

Stage 1 (Years 1-5): High-growth phase based on the user's specific G1 inputs.

Stage 2 (Years 6-10): A Linear Fade transition. The model calculates the annual step-down required to move from the G1 rate to the G2 rate, simulating natural market saturation and competitive convergence.

Stage 3 (Years 11-20): A mature growth phase based on the G3 input, capped to reflect long-term economic reality.

2. Terminal Value Calculation
To ensure a robust "Exit Value," the script calculates and averages two professional methods:

Gordon Growth Model: Calculates value based on a perpetual growth rate (typically capped at 2% to align with long-term GDP growth).

Exit Multiple Method: Applies a Price-to-Cash-Flow multiple (capped at 15x-20x for safety) to the final year's projected FCF.

Averaging: By averaging these two methods, the model provides a more "grounded" intrinsic value that isn't overly sensitive to a single terminal assumption.

3. Automated Data Pipeline
Financials: Uses yfinance to scrape real-time Operating Cash Flow, CapEx, Total Cash, and Total Debt.

WACC (Discount Rate): Dynamically calculates the discount rate based on the stock's Beta, adjusting the required return for the risk profile of the specific ticker.

Net Debt Adjustment: Subtracts Net Debt (Total Debt - Cash) from the Enterprise Value to arrive at the Equity Value, ensuring the final share price reflects the company's actual balance sheet.

🚀 How to Use This Dashboard
Clone the Repo: Download the .pbix and tickers_config.xlsx files.

Update Assumptions: Open the Excel file and change the G1, G2, or G3 growth rates for any ticker.

Update File Path:

Open the Power BI file.

Go to Transform Data -> Source (Python Script).

Change the file path variable to point to the location of the Excel file on your computer.

Refresh: Click Refresh in Power BI. The Python engine will fetch new Yahoo Finance data, apply your Excel growth rates, and update the visuals.
