from marketopen import *
from getData import *

import json

from datetime import datetime


STOCK = 'GOOG'

def main() -> None:
    print()
    print("-------- Starting bot for the day ------------"), print()

    if pre_market_open():
        print("Pre - NYSE is open")

    if regular_market_open():
        print("Regular - NYSE is open")

    if post_market_open():
        print("Post - NYSE is open")

    client = authenticate()
    now = datetime.now()
    position = get_position(client)

    print(now), print()


        # get current position
    print('HAS POSITION: ' + str(position))

        # get current price
    price = getprice(client, STOCK)

    print("Current price " + str(price))

    callOption = call_option_chain(client, STOCK)
    putOption = put_option_chain(client, STOCK)

    print("Call IV = " + str(getCallIV(callOption)))


if __name__=="__main__":
    main()
