# HangSengIndex Stocks Porfolio with SharpeRatio
 A portfolio which its aunual return around 73%. Get all stocks data of Hang Seng Index. Select 5 stocks by annual return and volatility. Use Sharpe Ratio to find the final portfolio. This program use stock data from 2015-2019 for stocks selection. And the test outcome is made by 2020-current data. Feel free to share your strategy. <br/>
 
 Language: Python 3.7<br/><br/>
 Package: matplotlib,
          pandas,
          numpy,
          futu-api<br/>


If you want to use get data function, please install futu api. The instrcution can be easily find online.<br/>

You can adjust the volatility value to get the higher profir. Be careful if the volality is over 80.<br/>

Let's see the output:<br/>

Initial Capital: $ 1,000,000 <br/>



Maximum Sharpe Ratio Portfolio Allocation

Annualised Return: 0.73<br/>
Annualised Volatility: 0.32
| StockCode | Ratio |
| --- | --- |
| `HK.02313` | 40.28 |
| `HK.00700` | 18.83 |
| `HK.01093` | 11.43 |
| `HK.00823` | 29.33 |
| `HK.02318` | 0.13 |
<br/>

<br/>
Minimum Volatility Portfolio Allocation

Annualised Return: 0.56<br/>
Annualised Volatility: 0.28
| StockCode | Ratio |
| --- | --- |
| `HK.02313` | 9.83 |
| `HK.00700` | 16.85 |
| `HK.01093` | 16.06 |
| `HK.00823` | 53.17 |
| `HK.02318` | 4.08 |
<br/>

Output<br/>
| StockCode | Annual Return |
| --- | --- |
| `HK.02313` | 0.381818 |
| `HK.00700` | 0.993902 |
| `HK.01093` | 0.427693 |
| `HK.00823` | -0.073807 |
| `HK.02318` | 0.852524 |

<br/>
Yearly Return in Money:<br/>
| StockCode | Maximum Shaper Ratio | Minimum Volatility |
| --- | --- | --- |
| `HK.02313` | 343396 | 83803 |
| `HK.00700` | 187151 | 167472 |
| `HK.01093` | 48885 | 68687 |
| `HK.00823` | -21648 | -39244 |
| `HK.02318` | 496 | -39244 |
<br/><br/>
Final Capital:<br/>
Max Shaper Ratio: 2116565.068493047<br/>
Min Shaper Ratio: 1592596.0715312362

