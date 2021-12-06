from webull import webull
import yfinance as yf
from dataparser import parser
import pprint



webull = webull()

cumulativeFlow = [0] * 5
dates = [0] * 5

#tickerList = ["EFX", "CDW", "ROK", "LHX", "KSU", "TT", "TRV", "WLTW", "TER", "SWK", "MSI", "VMC", "TROW", "URI", "CDNS", "FRC", "W", "SGEN", "ALB", "RNG", "TWLO", "U", "BILL"]
tickerList = ["EFX", "CDW", "ROK", "LHX", "KSU"]
#make this function happen whenever you initialize a new stock
#then make a function to get the data for today and append it to the end of the
#function. Make some cloud application run this program once a day at market close to start
#building a data base for stocks.

print()

try:
    tickerdict = parser.read_file("tickerlog.json")
except FileNotFoundError:
    tickerdict = { "tickers" : {} }


for ticker in tickerList:

    flowData = webull.get_capital_flow(ticker)
    print("-------------------------")
    print("Order Flow Data for: " + ticker)
    print("-------------------------")
    print()

    symbol = yf.Ticker(ticker)
    hist = symbol.history(period="1wk")
    stockFlow = [0] * 5

    if(tickerdict.get("tickers").get(ticker) == None):
        currentTicker = {ticker : {"Date" : {} }}
        tickerdict.get("tickers").update(currentTicker)

    for i in range(5):
        date = flowData.get("historical")[i].get("date")
        date = date[:4] + "-" + date[4:6] + "-" + date[6:]
        dates[i] = date
        print(date)
        stockFlow[i] = flowData.get("historical")[i].get("item").get("majorNetFlow")
        cumulativeFlow[i] += flowData.get("historical")[i].get("item").get("majorNetFlow")

        instFlow = round(stockFlow[i]/1000000, 2)

        print("    Institution Flow (Millions): " + str(instFlow))
        #print("    Open: $" + str(round(float(hist.get("Open")[i]), 2)))
        #print("    Close: $" + str(round(float(hist.get("Close")[i]), 2)))

        changeNum = round(float(hist.get("Close")[i]) - float(hist.get("Open")[i]),2)
        if(changeNum < 0):
            change = (str(changeNum))[:1] + "$" + (str(changeNum))[1:]
        else:
            change = "$" + str(changeNum)
        print("    Change: " + str(change))

        currDateFlow = {date : { "flow": str(instFlow), "change": str(changeNum)}}
        tickerdict.get("tickers").get(ticker).get("Date").update(currDateFlow)

    print()

parser.write_file("tickerlog.json", tickerdict)



print("Cumulative Flow for these Stocks")
print("If using for trading ideas, shows more consistency only when entering on reversals, not continuations")
print()

for i in range(5):
    print(dates[i])
    print("    " + str(round(cumulativeFlow[i]/1000000, 2)))


def updateAvgFlow(ticker):

    try:
        tickerdict = parser.read_file("tickerlog.json")
    except FileNotFoundError:
        print("No log exists")
        return

    if(tickerdict.get("tickers").get(ticker) == None):
        print("Ticker doesn't exist, can't get average flow")
        return

    currentTicker = tickerdict.get("tickers").get(ticker)
    print("doing " + ticker)

    totalFlow = 0
    totalEntries = 0

    for i in range(len(currentTicker.get("Date"))):
        dayFlow = abs(float((list(currentTicker.get("Date").items())[i][1]).get("flow")))
        if (dayFlow > 0):
            totalFlow += dayFlow
            totalEntries += 1

    avgFlow = {"flowAvg" : str(round((totalFlow / totalEntries), 2)) }
    currentTicker.update(avgFlow)

    parser.write_file("tickerlog.json", tickerdict)

for ticker in tickerList:
    updateAvgFlow(ticker)

def displayLog():
    try:
        tickerdict = parser.read_file("tickerlog.json")
    except FileNotFoundError:
        print("No log exists")
        return

    pprint.pprint(tickerdict)

displayLog()




#print(date.fromtimestamp(time.time()))
#print(date.fromtimestamp(time.time()-86400))
