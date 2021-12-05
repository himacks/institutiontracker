from dataparser import parser

nested_dict = { 'dictA': {'key_1': 'value_1'},
                'dictB': {'key_2': 'value_2'}}
tickerdict = { "tickers" : {"EFX" : {"Date" : { "2021-11-29" : { "flow": "1.2345", "change": "4.43"},
                                                "2021-11-30" : { "flow": "2.2345", "change": "5.43"}
                                              }
                                    }
                           }
             }

print(tickerdict.get("tickers").get("EFX").get("Date").get("2021-11-30").get("flow"))

parser.write_file("test.json", tickerdict)
