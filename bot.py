from marketopen import *
from data import *

import json

from datetime import datetime



STOCK = 'SPY'

def main() -> None:

    print()
    print("-------- Starting bot for the day --------"), print()

    if pre_market_open():
        print("Pre - NYSE is open")

    if regular_market_open():
        print("Regular - NYSE is open")

    if post_market_open():
        print("Post - NYSE is open")

    client = authenticate()
    now = datetime.now()
    position = get_position(client)

    print(now)


    # get current position
    #print('HAS POSITION: ' + str(position))

    # get current price
    price = getprice(client, STOCK)

    print("Current price " + str(price)), print()

    print("------ Call Options ------")
    print("Range / days to expiration is: " + str(DAYSOUT))
    callOption = call_option_chain(client, STOCK)
    callIV = getCallIV(callOption)
    print("Call IV Based On Freq = " + str(callIV))
    callexpected = expectedRange(callIV, DAYSOUT, price)
    print("Expected range +/- : " + str(callexpected))
    print("Expected stock range: " + str(callexpected + price) + " to " + str(price - callexpected))

    print()
    print("------ Put Options ------")
    print("Range / days to expiration is: " + str(DAYSOUT))
    putOption = put_option_chain(client, STOCK)
    putIV = getPutIV(putOption)
    print("Put IV based on Freq = " + str(putIV))
    putexpected = expectedRange(putIV, DAYSOUT, price)
    print("Expected range +/- : " + str(putexpected))
    print("Expected stock range: " + str(putexpected + price) + " to " + str(price - putexpected))


    #putOption = put_option_chain(client, STOCK)


    #print("Call IV = " + str(getCallIV(callOption))), print()
    #print("Put IV = " + str(getPutIV(putOption)))


if __name__=="__main__":
    main()
