from marketopen import *
from getData import *

from datetime import datetime


STOCK = 'SPY'

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

    print(now)


        # get current position
    print('HAS POSITION: ' + str(position))

        # get current price
    price = getprice(client, STOCK)

    print("Current price " + str(price))

    Calloption = call_option_chain(client, STOCK)
    Putoption = put_option_chain(client, STOCK)


if __name__=="__main__":
    main()
