# FinancialEngineering-FinalProject-SizeFactor
This is the final project of Financial Engineering (Tsinghua SEM, 2018 fall) on size factor in Chine. In this research, we used the stock information from China’s A-share market. The data base covers 3,631 stocks on China’s market, and the test period is from January 2005 to June 2018. 

# Getting Start
## Requirements
- python 3.7.1
- pandas>=0.23.4
- numpy>=1.15.4
- scipy>=1.1.0
- matplotlib>=3.0.2
- statsmodels>=0.9.0

## Clone Project
Run `Terminal` (for MacOS or Linux) / `Git Bash` (for Windows). Navigate to a proper directory. Clone our sever-side repository using:
``` 
git clone https://github.com/wangsiping97/FinancialEngineering-FinalProject-SizeFactor.git
```
## Setup Data
Copy `CadeDataAll.mat` to `FinancialEngineering-FinalProject-SizeFactor` directory.

To facilitate the loading with pandas, we transformed `ThreeFactorData.xlsx` to csv format (i.e., `ThreeFactorData.csv`) using excel.

Since the monthly return data ranges from 2000 to 2018 and the three factor data ranges from 2005 to 2018, to match the index conveniently, we added 60 empty rows before `ThreeFactorData.xlsx` and get `Market.csv`. 

# Usage

## Intermediate Files
- `post_yield.csv`, `post_beta.csv`, `post_betas.csv` are three intermediate files output to reduce the operation, output by the program `ComputePostBeta.py`.
- The correlation coefficient of size and beta is one of the data mentioned in the report, output by the program `CorrelationCoefficient.py`.

## Table1
- `table1.csv` is the result of Single Sorting and is output by the program `table1.py`.
- The output contains 7 columns: 
    - `Rt_EW`: Average Monthly Returns of Equal Weighted, is computed from line 28 to line 46
    - `Rt_VW`: Average Monthlyl Returns of Value Weighted, is computed from line 49 to line 72
    - `log_ME`: Average Log of Market Equity, is computed from line 75 to line 96
    - `log_BM`: Average Log of Book to Market Ratio, is computed from line 99 to line 121
    - `R_1`: Average Returns in January, is computed from line 124 to line 141
    - `R_12`: Average Returns in December, is computed from line 144 to line 161
    - `Mon_Illiq`: Average Monthly ILLIQ, is computed from line 164 to line 182

## Table2
- `table2.csv` is the result of Double Sorting and is output by the program `table2.py`. The output is divided into two files: `table2_return.csv` and `table2_tvalue.csv`. The former is the monthly average of each group, and the latter is the monthly mean t-value.

## Table3
- `table3.csv` calculates the alpha result for the CAPM model and is output by the program `table3.py`. The output is divided into two types: `table3_all.csv` and `table3_flt.csv`. The former is the result obtained by grouping the total market value, and the latter is the result of grouping by the market value of circulation.

## Table4
- `table4.csv` is the result of Fama-Macbeth regression. 
- The output is computed by `table4.py`.

## Table5
- `table5.csv` is the result of the Average Monthly Returns of each portfolio of longing Group-i and shorting Group-j for i in range (2, 10) and j in range (i + 1, 11), based on our size factor strategy. 
- The output is computed by `table5.py`.

## Table6
- `table6.csv` is the result of the Alpha of each portfolio of longing Group-i and shorting Group-j for i in range (2, 10) and j in range (i + 1, 11), based on our size factor strategy. 
- The output is computed by `table6.py`.

## Table7
- `table7.csv` is the result of the Anually Sharpe Ratio of each portfolio of longing Group-i and shorting Group-j for i in range (2, 10) and j in range (i + 1, 11), based on our size factor strategy. 
- The output is computed by `table7.py`.

## Table8
- `table8.csv` is the result of the Max Drawdown of each portfolio of longing Group-i and shorting Group-j for i in range (2, 10) and j in range (i + 1, 11), based on our size factor strategy. 
- The output is computed by `table8.py`.

## Figure1
- `figure1.png` is the Time Series Plot of Monthly Average of Firms' Size in China since 2005.
- The output is computed by `figure1.py`.

## Figure2
- `figure2.png` is the Time Series Plot of Monthly Skewness of Firms' Size in China since 2005.
- The output is computed by `figure2.py`.

## Figure3
- `figure3.png` is the Time Series Plot of Monthly Kurtosis of Firms' Size in China since 2005.
- The output is computed by `figure3.py`.

## Figure4
- `figure4.png` is the Time Series Plot of the Monthly Compounded Returns with portfolio: longing Group-2 and shorting Group-10.
- The output is computed by `figure4.py`.

## Lost-stop Strategy
- `table9.csv` (though not appeared on the paper) displays the result of the Ave_Rt, Alpha, Sharpe Ratio and Max Drawdown, and `figure5.png` is the Time Series Plot of the Monthly Compounded Returns of the portfolio of longing Group-2 and shorting Group-10 with a `lost-stop strategy` of eliminating stocks in `Group-2` that have returns `less than -0.1` in the previous `3` months when adjusting our positions each month. The variables abovementioned, `Group-2`, `less than -0.1` and `3` can all be adjusted. 
- The code of this simple lost-stop strategy is as following (take the portfolio of longing size-2 and shorting size-10 and `Group-2`, `less than -0.1` and `3` for an example): 
```
for i in range(60, 221): # Months since Jan. 2005
    a = pd.DataFrame(np.insert(mon[i - 3: i + 2], 1, values=size[i], axis=0))
    a = a.iloc[1:6].dropna(axis=1, how="any").T
    a = a.sort_values(by=1, ascending=True)
    unit = int(np.size(a[1]) / 10)
    unit_2 = a.iloc[unit:unit * 2]
    unit_2 = unit_2.loc[unit_2[4] >= -.1]
    unit_2 = unit_2.loc[unit_2[3] >= -.1]
    unit_2 = unit_2.loc[unit_2[2] >= -.1]
    unit_10 = a.iloc[unit * 9:]
    revenue[i - 60] = np.mean(unit_2[5]) - np.mean(unit_10[5]) # Compute the strategy monthly return
```
- The outputs are computed by `lost_stop.py`. 

#Author
- Kai Xiao, Haotian Xu, Siping Wang
- Github: https://github.com/wangsiping97