# HangSengIndex Stocks Porfolio with SharpeRatio
 A portfolio which its aunual return around 73%. Get all stocks data of Hang Seng Index. Select 5 stocks by annual return and volatility. Use Sharpe Ratio to find the final portfolio. This program use stock data from 2015-2019 for stocks selection. And the test outcome is made by 2020-current data. Feel free to share your strategy. <br/>
 
 Language: <h5>Python 3.7</h5><br/><br/>
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

HK.02313  HK.00700  HK.01093  HK.00823  HK.02318<br/>
40.28     18.83     11.43     29.33      0.13 

<br/>
Minimum Volatility Portfolio Allocation

Annualised Return: 0.56<br/>
Annualised Volatility: 0.28

HK.02313  HK.00700  HK.01093  HK.00823  HK.02318<br/>
9.83     16.85     16.06     53.17      4.08
<br/>

Output<br/>
         HK.00700  HK.00823  HK.01093  HK.02313  HK.02318
Changes  0.993902 -0.073807  0.427693  0.852524  0.381818

<br/>
Yearly Return in Money:<br/>
                      HK.02313  HK.00700  HK.01093  HK.00823  HK.02318
Maximum Shaper Ratio    343396    187151     48885    -21648       496
Minimum Volatility       83803    167472     68687    -39244     15578
<br/><br/>
Final Capital:<br/>
Max Shaper Ratio: 2116565.068493047
Min Shaper Ratio: 1592596.0715312362

