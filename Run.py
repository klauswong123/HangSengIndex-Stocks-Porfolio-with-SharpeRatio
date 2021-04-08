import numpy as np
import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt
from futu import *
import json
import datetime

class portfolioOptimazation:
    def __init__(self):
        self.voliList = []
        self.stocklist = []
        self.capital = 1000000
        # self.getMonthData()
        # self.getDayData()
        # self.getTestData()
        self.runProgram()

    def runProgram(self):
        self.dataset = pd.read_csv("DayData.csv",index_col='date')
        self.stockCodes = self.dataset.columns.tolist()
        self.volatilityList = self.getVolatility(self.dataset)
        self.yearlyReturn = self.getYearlyReturn(self.dataset)
        selectedCode = self.findStock()
        self.dataset = self.dataset[selectedCode]
        self.x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in self.dataset.index]
        self.returns = self.dataset.pct_change()
        self.mean_returns = self.returns.mean()
        self.cov_matrix = self.returns.cov()
        self.num_portfolios = 25000
        self.risk_free_rate = 0.103
        max_sharpe_allocation, min_vol_allocation = self.display_simulated_ef_with_random()
        self.dataset = pd.read_csv("testData.csv", index_col='date')
        self.dataset = self.dataset[selectedCode]
        self.yearlyReturn = self.getYearlyReturn(self.dataset)
        finalProfitMaxShaper = {}
        finalProfitMinVol={}
        maxshaProfit = 0
        minvolProfit = 0
        print("\n\nAnnually Return Per Stock")
        print(self.yearlyReturn)
        for i in selectedCode:
            finalProfitMaxShaper[i] = int((1+max_sharpe_allocation[i].values[0]/100*self.yearlyReturn[i].values[0])*self.capital)-self.capital
            maxshaProfit = maxshaProfit+(1+max_sharpe_allocation[i].values[0]/100*self.yearlyReturn[i].values[0]*2)*self.capital-self.capital
            finalProfitMinVol[i] = int((1+min_vol_allocation[i].values[0]/100 * self.yearlyReturn[i].values[0])*self.capital)-self.capital
            minvolProfit = minvolProfit + (1+min_vol_allocation[i].values[0]/100 * self.yearlyReturn[i].values[0]*2)*self.capital-self.capital
        df1 = pd.DataFrame(finalProfitMaxShaper, index=["Maximum Shaper Ratio"])
        df2 = pd.DataFrame(finalProfitMinVol, index=["Minimum Volatility"])
        frames = [df1, df2]
        result = pd.concat(frames)
        print("\n\nYearly Return in Money:")
        print(result)
        print("\nFinal Capital:")
        print(f'Max Shaper Ratio: {maxshaProfit + self.capital}')
        print(f'Min Shaper Ratio: {minvolProfit + self.capital}')

    def findStock(self):
        stockList0 =[]
        stockList2 = []
        changes1 = {'Changes': [],"Volatility":[]}
        index = []
        rankDictionary=sorted(self.yearlyReturn.to_dict(orient="int")['Changes'].items(), key=lambda x: x[1],reverse=True)
        for i in self.stockCodes:
            if self.yearlyReturn[i].values.tolist()[0]>0:
                stockList0.append(i)
            if self.volatilityList[i]<0.4:
                stockList2.append(i)
            if self.yearlyReturn[i].values.tolist()[0]>0 and self.volatilityList[i]<0.4:
                index.append(i)
                changes1['Changes'].append(self.yearlyReturn[i].values.tolist()[0])
                changes1['Volatility'].append(self.volatilityList[i])
        s1 = set(stockList0)
        s3 = set(stockList2)
        set1 = s1
        result_set = set1.intersection(s3)
        final_list = list(result_set)
        df1 = pd.DataFrame(changes1, index=index)
        df1['rank'] = df1['Changes'].rank(ascending=False)
        print(df1.sort_values(by="rank"))
        maxprofit = {}
        for i in rankDictionary:
            if i[0] in final_list:
                maxprofit[i[0]] = i[1]
        returnRank = []
        for i in maxprofit.keys():
            returnRank.append(i)
            if len(returnRank)==5:
                break
        return returnRank

    def getVolatility(self, dataset):
        vol = dataset.pct_change().apply(lambda x: np.log(1 + x)).std().apply(lambda x: x * np.sqrt(250))
        return vol

    def getYearlyReturn(self, dataset):
        changes = {}
        for i in self.stockCodes:
            try:
                data = dataset[i]
                changes[i]=(data[-1] -data[0])/data[0]
            except:
                pass
        df = pd.DataFrame(changes, index=["Changes"])
        return df

    def getMacd(self):
        dataset = pd.read_csv("MonthData.csv", index_col='date')
        date = dataset.index.values.tolist()
        macdSet = {}
        for i in self.stockCodes:
            try:
                data = dataset[i]
                macdlist = self.getMacdList(data)
                macd =  [macdlist[0][i]-macdlist[1][i] for i in range(0,len(macdlist[1]))]
                macdSet[i] = macd
            except Exception as e:
                print(e)
        df = pd.DataFrame(macdSet, index=date)
        df.index.name = 'date'
        #df.to_csv("MonthMACD.csv")
        self.stockCodes=df.columns.tolist()
        return df

    def showDailyReturn(self):
        returns = self.dataset.pct_change()
        plt.figure(figsize=(14, 7))
        for c in returns.columns.values:
            plt.plot(self.x_values, returns[c], lw=3, alpha=0.8, label=c)
        plt.legend(loc='upper right', fontsize=12)
        plt.ylabel('daily returns')
        plt.show()

    def showStockRecord(self):
        plt.figure(figsize=(14, 7))
        for c in self.dataset.columns.values:
            plt.plot(self.x_values, self.dataset[c], lw=3, alpha=0.8, label=c)
        plt.legend(loc='upper left', fontsize=12)
        plt.ylabel('price in $')
        plt.show()

    def display_simulated_ef_with_random(self):
        results, weights = self.random_portfolios(self.num_portfolios, self.mean_returns, self.cov_matrix, self.risk_free_rate)
        max_sharpe_idx = np.argmax(results[2])
        sdp, rp = results[0, max_sharpe_idx], results[1, max_sharpe_idx]
        max_sharpe_allocation = pd.DataFrame(weights[max_sharpe_idx], index=self.dataset.columns, columns=['allocation'])
        max_sharpe_allocation.allocation = [round(i * 100, 2) for i in max_sharpe_allocation.allocation]
        max_sharpe_allocation = max_sharpe_allocation.T
        min_vol_idx = np.argmin(results[0])
        sdp_min, rp_min = results[0, min_vol_idx], results[1, min_vol_idx]
        min_vol_allocation = pd.DataFrame(weights[min_vol_idx], index=self.dataset.columns, columns=['allocation'])
        min_vol_allocation.allocation = [round(i * 100, 2) for i in min_vol_allocation.allocation]
        min_vol_allocation = min_vol_allocation.T
        print("-" * 80)
        print("Maximum Sharpe Ratio Portfolio Allocation\n")
        print("Annualised Return:", round(rp, 2))
        print("Annualised Volatility:", round(sdp, 2))
        print("\n")
        print(max_sharpe_allocation)
        print("-" * 80)
        print("Minimum Volatility Portfolio Allocation\n")
        print("Annualised Return:", round(rp_min, 2))
        print("Annualised Volatility:", round(sdp_min, 2))
        print("\n")
        print(min_vol_allocation)
        plt.figure(figsize=(10, 7))
        plt.scatter(results[0, :], results[1, :], c=results[2, :], cmap='YlGnBu', marker='o', s=10, alpha=0.3)
        plt.colorbar()
        plt.scatter(sdp, rp, marker='*', color='r', s=500, label='Maximum Sharpe ratio')
        plt.scatter(sdp_min, rp_min, marker='*', color='g', s=500, label='Minimum volatility')
        plt.title('Simulated Portfolio Optimization based on Efficient Frontier')
        plt.xlabel('annualised volatility')
        plt.ylabel('annualised returns')
        plt.legend(labelspacing=0.8)
        plt.show()
        return max_sharpe_allocation, min_vol_allocation

    def random_portfolios(self,num_portfolios, mean_returns, cov_matrix, risk_free_rate):
        results = np.zeros((3, num_portfolios))
        weights_record = []
        for i in range(num_portfolios):
            weights = np.random.random(5)
            weights /= np.sum(weights)
            weights_record.append(weights)
            portfolio_std_dev, portfolio_return = self.portfolio_annualised_performance(weights, mean_returns, cov_matrix)
            results[0, i] = portfolio_std_dev
            results[1, i] = portfolio_return
            results[2, i] = (portfolio_return - risk_free_rate) / portfolio_std_dev
        return results, weights_record

    def portfolio_annualised_performance(self, weights, mean_returns, cov_matrix):
        returns = np.sum(mean_returns * weights) * 504
        std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(504)
        return std, returns

    def getTestData(self):
        self.quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
        try:
            stockCodes = pd.read_csv('./constituents.csv')['Symbol'].tolist()
            self.dataset = {}
            data1 = self.quote_ctx.request_history_kline('HK.00001', start="2019-01-24", end="2021-04-01",
                                                 ktype=KLType.K_DAY)[1]
            times=data1['time_key'].tolist()
            times = [a[:10] for a in times]
            for stockcode in stockCodes:
                try:
                    tempdata =self.quote_ctx.request_history_kline('HK.'+str(stockcode[1:-1]), start="2019-01-24", end="2021-04-01",
                                                                ktype=KLType.K_DAY)[1]
                    if len(tempdata) < 540:
                        continue
                    try:
                        self.dataset['HK.'+str(stockcode[1:-1])] = (tempdata['close'].tolist())

                    except Exception as e:
                        pass
                except Exception as e:
                    pass
            # for i in self.dataset:
            #     print(f"{i} : " + str(len(self.dataset[i])))
            print(self.dataset)
            df = pd.DataFrame(self.dataset, index=times)
            df.index.name = 'date'
            print(df)
            df.to_csv("TestData.csv")
        except Exception as e:
            print(e)
            pass
        self.quote_ctx.close()

    def getDayData(self):
        self.quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
        try:
            stockCodes = pd.read_csv('./constituents.csv')['Symbol'].tolist()
            self.dataset = {}
            data1 = self.quote_ctx.request_history_kline('HK.00001', start="2015-01-01", end="2020-01-01",
                                                 ktype=KLType.K_DAY)[1]
            times=data1['time_key'].tolist()
            times = [a[:10] for a in times]
            for stockcode in stockCodes:
                try:
                    tempdata =self.quote_ctx.request_history_kline('HK.'+str(stockcode[1:-1]), start="2015-01-01", end="2020-01-01",
                                                                ktype=KLType.K_DAY)[1]
                    if len(tempdata) < 1000:
                        continue
                    try:
                        self.dataset['HK.'+str(stockcode[1:-1])] = (tempdata['close'].tolist())
                    except Exception as e:
                        pass
                except Exception as e:
                    pass
            # for i in self.dataset:
            #     print(f"{i} : " + str(len(self.dataset[i])))
            print(self.dataset)
            df = pd.DataFrame(self.dataset, index=times)
            df.index.name = 'date'
            print(df)
            df.to_csv("DayData.csv")
        except Exception as e:
            print(e)
            pass
        self.quote_ctx.close()

    def getMonthData(self):
        self.quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
        try:
            stockCodes = pd.read_csv('./constituents.csv')['Symbol'].tolist()
            self.dataset = {}
            data1 = self.quote_ctx.request_history_kline('HK.00001', start="2015-01-01", end="2019-01-01",
                                                 ktype=KLType.K_MON)[1]
            times=data1['time_key'].tolist()
            times = [a[:10] for a in times]
            for stockcode in stockCodes:
                try:
                    tempdata =self.quote_ctx.request_history_kline('HK.'+str(stockcode[1:-1]), start="2015-01-01", end="2019-01-01",
                                                                ktype=KLType.K_MON)[1]
                    if len(tempdata) < 47:
                        continue
                    try:
                        self.dataset['HK.'+str(stockcode[1:-1])] = (tempdata['close'].tolist())
                    except Exception as e:
                        pass
                except Exception as e:
                    pass
            # for i in self.dataset:
            #     print(f"{i} : " + str(len(self.dataset[i])))
            print(self.dataset)
            df = pd.DataFrame(self.dataset, index=times)
            df.index.name = 'date'
            print(df)
            df.to_csv("MonthData.csv")
        except Exception as e:
            print(e)
            pass
        self.quote_ctx.close()

    def getMacdList(self, data):
        ema12List = self.calculate_EMA(data,12)
        ema26List = self.calculate_EMA(data,26)
        MACDList =  self.get_MACD(ema12List,ema26List,0)
        return MACDList

    def calculate_EMA(self, cps, days):
        emas = cps.copy()
        for i in range(len(cps)):
            if i == 0:
                emas[i] = cps[i]
            if i > 0:
                emas[i] = ((days - 1) * emas[i - 1] + 2 * cps[i]) / (days + 1)
        return emas

    def get_MACD(self,ema12List,ema26List,lastDea):
        diffList= []
        deaList = []
        lastdea= lastDea
        for i in range(len(ema12List)):
            diff = ema12List[i] - ema26List[i]
            dea = lastdea*0.8+diff*0.2
            lastdea = float(dea)
            diffList.append(diff)
            deaList.append(dea)
        return diffList,deaList

if __name__ == '__main__':
    a = portfolioOptimazation()