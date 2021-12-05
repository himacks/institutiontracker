from webull import webull
import yfinance as yf
from datetime import date
import time


webull = webull()

cumulativeFlow = [0] * 5
dates = [0] * 5

tickerList = ["EFX", "CDW", "ROK", "LHX", "KSU", "TT", "TRV", "WLTW", "TER", "SWK", "MSI", "VMC", "TROW", "URI", "CDNS", "FRC", "W", "SGEN", "ALB", "RNG", "TWLO", "U", "BILL"]

#make this function happen whenever you initialize a new stock
#then make a function to get the data for today and append it to the end of the
#function. Make some cloud application run this program once a day at market close to start
#building a data base for stocks.

print()

for ticker in tickerList:

    flowData = webull.get_capital_flow(ticker)
    print("-------------------------")
    print("Order Flow Data for: " + ticker)
    print("-------------------------")
    print()

    symbol = yf.Ticker(ticker)
    hist = symbol.history(period="1wk")
    stockFlow = [0] * 5

    for i in range(5):
        date = flowData.get("historical")[i].get("date")
        date = date[:4] + "-" + date[4:6] + "-" + date[6:]
        dates[i] = date
        print(date)
        stockFlow[i] = flowData.get("historical")[i].get("item").get("majorNetFlow")
        cumulativeFlow[i] += flowData.get("historical")[i].get("item").get("majorNetFlow")
        print("    Institution Flow (Millions): " + str(round(stockFlow[i]/1000000, 2)))
        #print("    Open: $" + str(round(float(hist.get("Open")[i]), 2)))
        #print("    Close: $" + str(round(float(hist.get("Close")[i]), 2)))

        changeNum = round(float(hist.get("Close")[i]) - float(hist.get("Open")[i]),2)
        if(changeNum < 0):
            change = (str(changeNum))[:1] + "$" + (str(changeNum))[1:]
        else:
            change = "$" + str(changeNum)
        print("    Change: " + str(change))
    print()

print("Cumulative Flow for these Stocks")
print("If using for trading ideas, shows more consistency only when entering on reversals, not continuations")
print()

for i in range(5):
    print(dates[i])
    print("    " + str(round(cumulativeFlow[i]/1000000, 2)))


#print(date.fromtimestamp(time.time()))
#print(date.fromtimestamp(time.time()-86400))
