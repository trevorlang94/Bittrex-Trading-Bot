import requests
from BotFunctions import tradeBot
from time import sleep



hasHelped = False #changes menu text based on if you've used it already. Might be a sloppy way of doing this
menuString = '\nWhat can I do for you?'

trader = tradeBot()

print('Hello, I am your personal trading assistant!')
print('Enter your Bittrex API key: ')
apiKey = input()


while(True):
    if(hasHelped == True):
        menuString = '\nWhat else can I do for you?'
        
    print(menuString + '\n 1 - Look Up Market (Format: \"BTC-ETH\") \n 2 - Display all Listed Cryptocurrencies \n 3 - What\'s Dropping \n 0 - Exit \n')
    menuOption = int(input())

    if (menuOption == 1):
        trader.marketLookup()
    elif(menuOption == 2):
        trader.getAllCurrencies()
    elif(menuOption == 3):
        trader.whatsDropping()
    elif (menuOption == 0):
        print("Exiting..")
        sleep(3)
        exit()

    hasHelped = True

    
        


