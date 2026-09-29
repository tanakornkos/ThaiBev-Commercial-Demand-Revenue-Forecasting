# ThaiBev Stock Forecasting: Market Momentum, Technical Indicators & Macroeconomic Drivers

Econometric and quantitative forecasting study for Thai Beverage Public Company Limited (`Y92.SI`), listed on the Singapore Exchange (SGX), evaluating price persistence, technical indicators, Thailand nationwide beer-sales data, and macroeconomic variables.

## Project Overview

This repository investigates whether ThaiBev stock returns and price trajectories can be forecast using:

- **Historical Price Behavior & Momentum**: Daily and monthly lagged returns.
- **Leak-Free Technical Indicators**: Monthly RSI and MACD features strictly lagged relative to forward targets.
- **Thailand Nationwide Beer-Sales Data**: Macroeconomic industry data adjusted for official 1-to-2 month publication delays.
- **Macroeconomic Drivers**: Singapore market benchmark (Straits Times Index `^STI`), Thai equity market proxy (iShares MSCI Thailand ETF `THD`), foreign exchange rates (`SGDTHB=X`), and COVID-19 lockdown regime indicators.
- **Small-Sample Models & Baselines**: Random walk baselines, regularized linear models (Ridge, ElasticNetCV), and SARIMAX with exogenous variables.

---

## Critical Methodological Improvements & Bug Fixes

1. **Elimination of Lookahead Leakage in Moving Averages**:
   - *Previous Bug*: The baseline computed `Close_ma_2 = Close.rolling(2).mean()`, averaging $Close_{t-1}$ and $Close_t$. Because the forecast for $Close_t$ directly included $Close_t$, it artificially achieved a near-zero MAPE (`0.0041`).
   - *Corrected Formulation*: Shifted strictly prior to rolling window:
     ```python
     Close_ma_2 = Close.shift(1).rolling(2).mean()
     Close_ema_5 = Close.shift(1).ewm(span=EMA_SPAN, adjust=False).mean()
     ```
   - *Recalculated Baseline*: The honest, un-leaked MA2 baseline exhibits a daily MAPE of **`0.0099`** and EMA5 exhibits **`0.0120`**, correctly trailing the simple Lag-1 persistence baseline (**`0.0094`**).

2. **Elimination of Technical Indicator Lookahead Bias**:
   - Monthly RSI and MACD were previously calculated using the target month's close. Features are now strictly lagged (`RSI_lag_1`, `MACD_hist_lag_1`) relative to the forward prediction horizon.

3. **Target Reformulation (Forward Return vs. Price Level Persistence)**:
   - Predicting raw stock prices ($P_t$) in financial time series spuriously rewards models that mimic unit-root persistence ($P_t \approx P_{t-1}$).
   - The primary monthly target is reformulated to:
     - **1-Month Forward Return**: $R_{t+1} = \frac{Close_{t+1}}{Close_t} - 1$ (`target_next_return`)
     - **Forward Return Direction**: $\mathbb{I}(R_{t+1} > 0)$ (`target_next_direction`)
     - **Excess Return over Straits Times Index**: $R_{t+1}^{ThaiBev} - R_{t+1}^{STI}$ (`target_relative_return`)

4. **Modeling Official Publication Delays for Beer Sales**:
   - Nationwide economic statistics in Thailand are compiled with a **45-to-60 day reporting lag**. An investor trading at month-end $t$ does not have access to month $t$ sales data.
   - We evaluate realistic publication lags:
     - `sale_lag_1`: Optimistic 1-month reporting lag.
     - `sale_lag_2`: Realistic conservative 2-month reporting lag.
     - `sale_yoy_growth_lag_2`: $\frac{Sale_{t-2} - Sale_{t-14}}{Sale_{t-14}}$ (deseasonalized and respecting publication delays).
     - `sale_rolling_3m_lag_2`: 3-month smoothed domestic beer sales proxy lagged by 2 months.

5. **Unified Daily Evaluation Windows**:
   - All daily baselines and models are evaluated on the exact same holdout period (**final 280 trading days**).

6. **Nested Model Ablation on Small Monthly Sample**:
   - Avoids deep learning on $N \approx 72$ monthly observations. Evaluates incremental value across nested specifications:
     - **Model A**: Price Momentum
     - **Model B**: Price Momentum + Technicals
     - **Model C**: Price Momentum + Beer Sales (2-month lag)
     - **Model D**: Price Momentum + Beer Sales + Macro & Regime Drivers
     - **SARIMAX**: Time series model with exogenous beer sales growth

---

## Dataset Documentation: Thai Beer Sales (`beer_sales_monthly.csv`)

| Metadata Field | Specification |
| :--- | :--- |
| **Original Source** | Bank of Thailand (BOT) Economic Statistics / Ministry of Finance Excise Department / Office of Industrial Economics (OIE) |
| **Download / Archive Date** | Captured series covering `2016-01` to `2023-03` |
| **Geographic Scope** | Domestic Kingdom of Thailand |
| **Measurement Nature** | Aggregate monthly retail/wholesale sales value of beer |
| **Currency & Units** | Thai Baht (THB), nominal value (averaging 8–16 billion THB/month) |
| **Licensing** | Thailand Open Government Data License / Public Domain |
| **Publication Schedule** | Published monthly with a **45 to 60 day delay** (compiled 1–2 months after month-end) |

### Essential Economic Distinction: Industry Sales vs. ThaiBev Revenue

> [!IMPORTANT]
> **Nationwide beer sales must not be conflated with ThaiBev company revenue:**
> 1. **Market Share**: ThaiBev (producer of Chang Beer) controls approximately 35%–40% domestic beer market share in Thailand, competing against Boon Rawd Brewery (Singha and Leo).
> 2. **Product Diversification**: ThaiBev derives major earnings from its high-margin **domestic spirits** division (SangSom, Mekhong, Ruang Khao, holding >80% domestic share), food franchises, and non-alcoholic beverages (Oishi green tea, F&N).
> 3. **International Footprint**: ThaiBev owns Sabeco (Bia Saigon), the largest brewer in Vietnam, as well as Scotch whisky distilleries in the UK and spirits producers in Myanmar.
> 
> Therefore, domestic Thai beer sales serve as an industry sentiment proxy rather than a direct top-line proxy for ThaiBev's consolidated enterprise earnings.

---

## Repository Contents

| File | Description |
| :--- | :--- |
| `thaibev_stock_forecasting.ipynb` | Comprehensive analysis notebook with daily and monthly leak-free models. |
| `beer_sales_monthly.csv` | Monthly Thai beer-sales data from `2016-01` to `2023-03` (87 rows). |
| `requirements.txt` | Python dependencies including `scikit-learn` and `statsmodels`. |
| `README.md` | Full project documentation and recalculated empirical results. |

---

## Methodology & Model Specifications

### Daily Forecasting Workflow
1. Ingest daily price history for `Y92.SI` from `2016-01-01` to `2023-04-01` (1,823 trading days).
2. Calculate leak-free shifted moving averages (`Close_ma_2`, `Close_ema_5`) and technical indicators.
3. Hold out the final 280 trading days (`2022-02-18` to `2023-03-31`) as a unified test set.
4. Benchmark Lag-1, shifted MA2, shifted EMA5, linear regression, ARIMA(0,1,0), and Exponential Smoothing.

### Monthly Forecasting Workflow
1. Aggregate daily stock prices and macro assets (`^STI`, `THD`, `SGDTHB=X`) to month-end observations.
2. Formulate 1-month forward return targets ($R_{t+1}$).
3. Engineer price momentum, lagged technical indicators, publication-lagged beer metrics, and macroeconomic returns.
4. Reserve the final 18 months (`2021-09` to `2023-02`) as the out-of-sample test window.
5. Execute nested model comparison using regularized regression (Ridge, ElasticNetCV) and SARIMAX.

---

## Recalculated Empirical Results

### 1. Daily Models (Unified 280-Day Test Window: `2022-02-18` to `2023-03-31`)

| Model | Specification | MAPE | Notes |
| :--- | :--- | ---: | :--- |
| **Lag-1 baseline** | $Close_{t-1}$ | **`0.0094`** | Random walk benchmark |
| **Lagged-close linear regression** | OLS on $Close_{t-1}$ | `0.0098` | Simple autoregressive fit |
| **MA2 baseline (leak-free)** | $\text{mean}(Close_{t-2}, Close_{t-1})$ | **`0.0099`** | Recalculated (was leaked `0.0041`) |
| **EMA5 baseline (leak-free)** | Shifted 5-day EMA | **`0.0120`** | Recalculated (was leaked `0.0074`) |
| **Exponential smoothing** | Holt-Winters damped additive | `0.0645` | Multi-step forecast degradation |
| **ARIMA** | $(0, 1, 0) \times (1, 0, 1)_8$ | `0.0660` | Multi-step forecast degradation |

*Observation*: Once lookahead leakage is resolved, MA2 error more than doubles (from `0.0041` to `0.0099`), confirming that daily market prices are best approximated by a random walk where smoothing introduces lag.

---

### 2. Monthly Return Models (Unified 18-Month Test Window: `2021-09` to `2023-02`)

*Target: 1-Month Forward ThaiBev Return ($R_{t+1}$)*

| Model | Feature Group | Out-of-Sample RMSE | Out-of-Sample MAE | Directional Accuracy | IC Correlation |
| :--- | :--- | ---: | ---: | ---: | ---: |
| **SARIMAX (AR1 + Beer Exog)** | AR(1) + `sale_yoy_growth_lag_2` | **`0.0543`** | **`0.0435`** | **`66.67%`** | **`0.4426`** |
| **Zero-Return Baseline** | $E[R_{t+1}] = 0$ | `0.0554` | `0.0444` | `61.11%` | `0.0000` |
| **Historical Mean Baseline** | $E[R_{t+1}] = \bar{R}_{train}$ | `0.0555` | `0.0444` | `61.11%` | `0.0000` |
| **Model C: Price + Beer Sales** | Returns + Beer Lags | `0.0560` | `0.0446` | `55.56%` | `0.1086` |
| **Model A: Price Momentum** | `return_1m`, `return_2m`, `return_3m` | `0.0566` | `0.0459` | `50.00%` | `0.0705` |
| **Model D: Price + Beer + Macro** | Model C + STI, THD, FX, COVID | `0.0640` | `0.0495` | `55.56%` | `0.1125` |
| **Model B: Price + Technicals** | Model A + RSI, MACD | `0.0920` | `0.0658` | `61.11%` | `-0.0113` |

---

## Incremental Value Assessment & Honest Research Findings

1. **Does Beer Sales Data Add Incremental Value?**
   - **Contemporaneous vs. Lagged Realities**: While unlagged beer sales exhibit artificial correlation with stock returns, this signal evaporates when respecting the realistic 2-month publication schedule (`sale_lag_2` correlation = `-0.0456`).
   - **Deseasonalized Growth Signal**: Deseasonalized annual growth (`sale_yoy_growth_lag_2`) combined with autoregressive modeling in **SARIMAX** achieved the lowest test RMSE (**`0.0543`**) and highest directional hit rate (**`66.67%`**), outperforming both the Zero-Return baseline and standalone price momentum.
   - **Economic Explanation**: Beer sales provide a broad macroeconomic health pulse of domestic Thai consumer spending, but cannot act as a high-frequency trading trigger.

2. **The Curse of Dimensionality in Small Samples**:
   - In monthly datasets with $N \approx 72$, adding too many features (Model B technicals or Model D unregularized macro factors) inflates out-of-sample variance, causing RMSE to degrade from `0.0560` to `0.0640` and `0.0920`.
   - **Autoregressive Mean Reversion**: Monthly returns display significant negative serial correlation ($\text{AR1} = -0.2625, p = 0.039$), rewarding parsimonious mean-reverting models over trend followers.

3. **Conglomerate Diversification**:
   - Because ThaiBev's revenue and operating profits are heavily supported by domestic spirits (Mekhong/SangSom) and international beer (Sabeco in Vietnam), fluctuations in domestic Thai beer volume only partially influence consolidated enterprise valuation.

---

## Installation & Environment

Create and activate a virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

Core dependencies:
```
numpy
pandas
matplotlib
seaborn
yfinance
requests
statsmodels
scipy
scikit-learn
```

---

## Usage

1. Open `thaibev_stock_forecasting.ipynb`.
2. Verify parameters in Section 2 (`TICKER`, `START_DATE`, `END_DATE`, `DAILY_TEST_DAYS`, `MONTHLY_TEST_MONTHS`).
3. Run all cells top-to-bottom.
4. Review the leak-free daily benchmarks and the nested monthly return forecasting tables.
