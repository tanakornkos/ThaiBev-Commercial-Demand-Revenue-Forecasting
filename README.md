# ThaiBev Stock Price Forecasting

Forecasting project for Thai Beverage Public Company Limited (`Y92.SI`) using Yahoo Finance stock prices, technical indicators, and monthly Thai beer-sales data.

## Project Overview

This analysis evaluates whether ThaiBev stock prices can be forecast from:

- Historical close-price behavior.
- Technical indicators, including RSI and MACD.
- Monthly beer-sales values.
- Classical time-series baselines such as moving average, ARIMA, and exponential smoothing.

The notebook is structured for reproducibility: key parameters are defined in one configuration cell, file names are stable, and results are summarized with mean absolute percentage error (MAPE).

## Repository Contents

| File | Description |
| --- | --- |
| `thaibev_stock_forecasting.ipynb` | Main analysis notebook. |
| `beer_sales_monthly.csv` | Monthly Thai beer-sales data from `2016-01` to `2023-03`. |
| `requirements.txt` | Python dependencies for running the notebook. |
| `README.md` | Project documentation. |

## Data Sources

| Dataset | Source | Frequency | Date Range |
| --- | --- | --- | --- |
| ThaiBev stock prices (`Y92.SI`) | Yahoo Finance via `yfinance` | Daily | `2016-01-01` to `2022-01-01` |
| Thai beer-sales value | Local CSV file | Monthly | `2016-01` to `2023-03` |

The stock data is aggregated to month-end observations before it is merged with the monthly beer-sales dataset.

## Methodology

The notebook follows this workflow:

1. Configure project parameters such as ticker, date range, train/test windows, and model settings.
2. Download daily stock prices from Yahoo Finance.
3. Load monthly beer-sales data from `beer_sales_monthly.csv`.
4. Engineer price-history and technical-indicator features.
5. Evaluate daily forecasting baselines and time-series models.
6. Aggregate daily stock prices to monthly rows.
7. Compare monthly beer-sales regression against MACD, RSI, lagged close-price, moving-average, and exponential-smoothing models.

## Key Parameters

The main notebook parameters are grouped near the top of `thaibev_stock_forecasting.ipynb`.

| Parameter | Default | Purpose |
| --- | --- | --- |
| `TICKER` | `Y92.SI` | Yahoo Finance ticker. |
| `START_DATE` | `2016-01-01` | First stock-price date requested. |
| `END_DATE` | `2022-01-01` | End date for stock-price download. |
| `DAILY_TEST_DAYS` | `280` | Number of daily rows held out for testing. |
| `MONTHLY_TEST_MONTHS` | `12` | Number of monthly rows held out for testing. |
| `EMA_SPAN` | `5` | Exponential moving-average span. |
| `RSI_WINDOW` | `14` | RSI calculation window. |
| `ARIMA_ORDER` | `(0, 1, 0)` | Daily ARIMA order. |
| `ARIMA_SEASONAL_ORDER` | `(1, 0, 1, 8)` | Daily seasonal ARIMA order. |

## Results

Validation was run after refactoring the project files and notebook.

### Daily Models

| Model | MAPE |
| --- | ---: |
| MA2 baseline | `0.0041` |
| EMA5 baseline | `0.0074` |
| Lag-1 baseline | `0.0083` |
| Lagged-close linear regression | `0.0098` |
| Exponential smoothing | `0.0529` |
| ARIMA | `0.0592` |

### Monthly Models

Monthly results use the final 12 months as the test set.

| Model | MAPE |
| --- | ---: |
| MA2 baseline | `0.0250` |
| Lagged-close linear regression | `0.0581` |
| Exponential smoothing | `0.0762` |
| RSI linear regression | `0.1431` |
| Beer-sales linear regression | `0.1643` |
| MACD linear regression | `0.1848` |

The monthly moving-average baseline performed best in the current run. Beer sales alone was less predictive than recent stock-price behavior, but it remains useful as a business-context feature for future multivariate modeling.

## Installation

Create and activate a Python environment, then install dependencies:

```bash
pip install -r requirements.txt
```

If you prefer installing packages manually:

```bash
pip install numpy pandas matplotlib seaborn yfinance requests statsmodels scipy
```

## Usage

1. Open `thaibev_stock_forecasting.ipynb`.
2. Confirm the parameter cell matches the desired ticker, date range, and file path.
3. Run the notebook from top to bottom.
4. Review the daily and monthly MAPE tables.

The notebook creates a local `.yfinance_cache/` folder during execution. This cache is ignored by Git and can be deleted safely.

## Notes

- Results may change slightly if Yahoo Finance revises historical data.
- The notebook uses `yfinance` first and falls back to Yahoo's chart API if the primary download returns no rows.
- The current regressions are intentionally simple and interpretable.
- A natural next step is a multivariate monthly model that combines lagged close price, beer sales, MACD, RSI, and broader economic variables.
