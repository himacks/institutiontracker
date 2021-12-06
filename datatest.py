from dataparser import parser

tickerdict = { "tickers" : {} }

currentTicker = {"EFX" : {"Date" : {} } }

tickerdict.get("tickers").update(currentTicker)

testDateFlow1 = {"2021-11-29" : { "flow": "1.2345", "change": "4.43"}}
testDateFlow2 = {"2021-11-30" : { "flow": "2.2345", "change": "5.43"}}
testDateFlow3 = {"2021-12-01" : { "flow": "3.2345", "change": "4.43"}}


tickerdict.get("tickers").get("EFX").get("Date").update(testDateFlow1)

print(tickerdict.get("tickers").get("banana"))

parser.write_file("test.json", tickerdict)
