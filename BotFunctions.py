import requests
from time import sleep

#'e' is the arbitrary name we'll use for JSON responses

class tradeBot():
        
        repeat = True
        alphabetizedCurrencyList = [] #List which holds all currency names short/long sorted
        tickersList = [] #holds tickers to be combined with base currencies for price data

        oldPriceData = {}
        currentPriceData = {} #These store data used in the whatsDropping function


        def __init__(self):
                self.name = 'Trader'
        
        def repeatQuery(repeatVar):
                lookUpAgain = input('Search for another currency? Y/N\n').upper()
                print('lookUpAgain = ' + lookUpAgain + '\n')
                if lookUpAgain == 'N':
                        repeatVar = False
                        print(repeatVar)
                elif lookUpAgain == 'Y':
                        repeatVar = True
                else:
                        print('Invalid entry. Enter Y or N.\n')
                        repeatQuery(repeatVar)
                
        def marketLookup(self):
                query = 'https://bittrex.com/api/v1.1/public/getmarketsummary?market='
                market_to_search = input('Which market would you like to access?\n')            
                query += market_to_search
                base_Currency = market_to_search.split('-') #This is to let the user know which currency they are viewing their results in

                r = requests.get(query)
                if(r):
                        e = r.json()
                        f = e['result'][0]['MarketName']
                        print('\nMarket Name: '+ str(f))
                        f = e['result'][0]['High']
                        print('High: '+ str(format(float(f), '.8f')) + " " + base_Currency[0])
                        f = e['result'][0]['Low']
                        print('Low: '+ str(format(float(f), '.8f')) + " " + base_Currency[0])
                        f = e['result'][0]['Bid']
                        print('Bid: '+ str(format(float(f), '.8f')) + " " + base_Currency[0])
                        f = e['result'][0]['Ask']
                        print('Ask: '+ str(format(float(f), '.8f')) + " " + base_Currency[0])
                        f = e['result'][0]['Volume']
                        print('Volume: '+ str(float(f)))
                        f = e['result'][0]['TimeStamp']
                        print('Time Stamp: '+ str(f))
                        f = e['result'][0]['OpenBuyOrders']
                        print('Open Buy Orders: '+ str(f))
                        f = e['result'][0]['OpenSellOrders']
                        print('Open Sell Orders: '+ str(f) + '\n')
                

        def getAllCurrencies(self):
                query = 'https://bittrex.com/api/v1.1/public/getcurrencies'
                r = requests.get(query)
                e = r.json()
                currencyListLength = len(e['result'])

                try:
                        for i in range(0, currencyListLength - 1):
                                f = e['result'][i]['Currency'] + ' - ' + e['result'][i]['CurrencyLong']
                                self.alphabetizedCurrencyList.append(f)
         
                except Exception as e:
                        print("Error displaying currencies. (Exception type: " + e.__class__.__name__ + ")\n")

                self.alphabetizedCurrencyList.sort()
                
                #Display sorted list
                divCounter = 0 #counter for when to add a linebreak when displaying currencies
                for i in range(0, currencyListLength - 1):
                        if(divCounter/3 == 1):
                                self.tickersList.append(self.alphabetizedCurrencyList[i].split(" ")[0])
                                print(self.alphabetizedCurrencyList[i])
                                print('-----------------------------------------------------------------------------')
                                divCounter = 0
                        else:
                                self.tickersList.append(self.alphabetizedCurrencyList[i].split(" ")[0])
                                print(self.alphabetizedCurrencyList[i] + "*|*", end="")
                                divCounter += 1

        def whatsDropping(self):
                
                looping = True
                cycleTime = int(input('Wait how long between reports? Answer in number of seconds (300 is 5 mins).\n'))
                
                if(len(self.alphabetizedCurrencyList) == 0): #This function pulls from a list of tickers which is generated by getAllCurrencies()
                                print('Ticker list has not been populated.. attempting to grab all listed currency tickers.\n')
                                sleep(1)
                                self.getAllCurrencies()
                                sleep(1)
                                if(len(self.alphabetizedCurrencyList) > 0):
                                        print('Success!\n')
                                else:
                                        print('Error populating ticker list.')
                                        return
                                sleep(1) #sleep to give time to read output

                while(looping):                         

                        query = 'https://bittrex.com/api/v1.1/public/getmarketsummaries'
                        req = requests.get(query)
                        e = req.json()
                        resultLength = len(e['result'])

                        for x in range (0, (resultLength - 1)):

                                currencyGet = e['result'][x]['MarketName']
                                latestPrice = e['result'][x]['Last']

                                if((currencyGet in self.currentPriceData) == False):
                                        self.currentPriceData[currencyGet] = latestPrice

                                elif(currencyGet in self.currentPriceData and (latestPrice != self.currentPriceData[currencyGet])):
                                        self.oldPriceData[currencyGet] = self.currentPriceData[currencyGet]
                                        self.currentPriceData[currencyGet] = latestPrice

                        for x in range(0, (resultLength - 1)):
                                currencyGet = e['result'][x]['MarketName']

                                newerPrice = self.currentPriceData[currencyGet]
                                try:
                                        olderPrice = self.oldPriceData[currencyGet]
                                except Exception as ex:
                                        olderPrice = newerPrice

                                if(newerPrice < olderPrice):
                                        percentChange = ((olderPrice - newerPrice) / olderPrice) * 100
                                        print(currencyGet + ' has shifted by ' + str('{0:.3g}'.format(percentChange)) + '% to ' + str('{0:.10}'.format(newerPrice)) + ' ' + str(currencyGet.split('-')[0]))

                        print('Report finished.. refreshing price changes in ' + str(cycleTime) + ' seconds.')
                        print('----------------------------------------------------------------------------------------------')
                        sleep(cycleTime)
                        
                
                



