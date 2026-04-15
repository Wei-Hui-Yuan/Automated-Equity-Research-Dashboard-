import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import logging

#PHASE 1:

#Check if stock pass 5yrs growth in rev,net income and cash flow from operations
def check_growth(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    income_statement = ticker.financials
    cash_flow = ticker.cashflow
    metrics_to_check = [
    (income_statement, 'Total Revenue'),
    (income_statement, 'Net Income'),
    (cash_flow, 'Operating Cash Flow')
    ]
    growth_result = {}
    for df, label in metrics_to_check:
        series = df.loc[label][::-1].pct_change().dropna()
        is_growing = (series > 0).all()

        growth_result[label] = is_growing
    
    if all(growth_result.values()):
        print('Pass last 5 years growth in rev, cash flow and net income')
        return True
    else:
        print('One or more metric shows a decline')
        return False

#Get discount rate which is the opportunity cost of investing our cash in the specific company
#when we could have invested it in somewhere else with similar risk
def get_discount_rate(beta):
    risk_table = {
        0.8: 0.054,
        0.9: 0.057,
        1.0: 0.060,
        1.1: 0.063,
        1.2: 0.066,
        1.3: 0.069,
        1.4: 0.072,
        1.5: 0.075,
        1.6: 0.078
    }

    if beta < 0.8:
        return 0.054
    if beta >= 1.6:
        return 0.078
    
    closest_beta = round(beta, 1)
    beta_val = risk_table.get(closest_beta, 0.07) # Default to 7% if not found
    return beta_val + 0.02

def intrinsic_DCF(ticker_symbol, g1, g2, g3):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    
    beta = info.get('beta', 1.0)
    discount_rate = get_discount_rate(beta) 
    
    # 2. Free Cash Flow (OCF - CapEx)
    try:
        # use the most recent fiscal year data
        ocf = ticker.cashflow.loc['Operating Cash Flow'].iloc[0]
        capex = abs(ticker.cashflow.loc['Capital Expenditure'].iloc[0])
        current_fcf = ocf - capex
        


    except Exception as e:
        return None

    fcf_projections = []
    # Years 1-5 (G1)
    for i in range(1, 6):
        fcf_projections.append(current_fcf * (1 + g1)**i)
    # Years 6-10 (G2)
    current_growth = g2
    avg_decrease = (g2 - g2) /5
    for i in range(1, 6):
        current_growth -= avg_decrease
        fcf_projections.append(fcf_projections[-1] * (1 + current_growth))
    # Years 11-20 (G3)
    for i in range(1, 11):
        fcf_projections.append(fcf_projections[-1] * (1 + g3))

    # 4. Present Value Calculation
    pv_fcf = sum([fcf / (1 + discount_rate)**(i + 1) for i, fcf in enumerate(fcf_projections)])

    # 5. Averaged Terminal Value
    # Gordon Growth
    tv_g = (fcf_projections[-1] * 1.02) / (discount_rate - 0.02)
    # Exit Multiple (Capped at 20x for safety)
    exit_mult = min(info.get('priceToCashFlow', 15), 15)
    tv_e = fcf_projections[-1] * exit_mult
    
    avg_tv_pv = ((tv_g + tv_e) / 2) / (1 + discount_rate)**20

    # 6. Enterprise Value to Equity Value
    enterprise_value = pv_fcf + avg_tv_pv
    net_debt = info.get('totalDebt', 0) - info.get('totalCash', 0)
    equity_value = enterprise_value - net_debt
    
    shares = info.get('sharesOutstanding')
    intrinsic_val = round(equity_value / shares,2)
    print(f'{ticker} Instrinsic Value is: {intrinsic_val}  ')
    return equity_value / shares if shares else None


#calculating each stocks instrinsic value
config_df = config_df = pd.read_excel('tickers_config.xlsx', sheet_name='Sheet1')
final_results = []

logging.basicConfig(
    filename='valuation_log.txt', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)


for index,row in config_df.iterrows():
    ticker = row['Ticker']
    g1,g2,g3 = row['G1 (1-5y)'], row['G2 (6-10y)'], row['G3 (11-20y)']

    try:
        intrinsic_val = intrinsic_DCF(ticker,g1,g2,g3)

        stock_info = yf.Ticker(ticker).info
        price = stock_info.get('currentPrice')

        final_results.append({'Ticker': ticker,
            'Intrinsic Value': round(intrinsic_val, 2),
            'Market Price': price,
            'Upside %': round(((intrinsic_val / price) - 1), 2)})
        
    

    except Exception as e:
        error_msg = f"❌ Error on {ticker}: {e}"
        print(error_msg)
        logging.error(error_msg)
        continue

output_df = pd.DataFrame(final_results)
output_df.to_csv('equity_research_output.csv',index = False)





