from tda import auth, client
from webdriver_manager.chrome import ChromeDriverManager
from auth_params import ACCT, API, CALLBACK
from selenium import webdriver

import math
import numpy as np

from datetime import date, timedelta

import json

CHAINSIZE = 30
DAYSOUT = 2

#used to authenticate client
def authenticate():
    token_path = 'aaah.json'
    try:
        client = auth.client_from_token_file(token_path, API)
    except FileNotFoundError:
        with webdriver.Chrome(ChromeDriverManager().install()) as driver:
            client = auth.client_from_login_flow(
                driver, API, CALLBACK, token_path)
    return client

#returns last price of ticker
def getprice(client, ticker: str):
    r = client.get_quote(ticker)
    assert r.status_code == 200, r.raise_for_status()

    y = r.json()
    price = y[ticker]["lastPrice"]
    return price

#returns positions
def get_position(client):
    r = client.get_account(ACCT, fields=client.Account.Fields.POSITIONS)
    assert r.status_code == 200, r.raise_for_status()

    out = r.json()

    if "positions" in out["securitiesAccount"]:
        return True
    else:
        return False

#get the call options chain
def call_option_chain(client, ticker: str):
    expDate = date.today() + timedelta(DAYSOUT)
    #strike_range=client.Options.StrikeRange.NEAR_THE_MONEY, if you want NTM
    r = client.get_option_chain(
        symbol=ticker,
        contract_type=client.Options.ContractType.CALL,
        to_date=expDate,
        from_date=date.today(),
        strike_count=CHAINSIZE,
        strategy=client.Options.Strategy.ANALYTICAL
        )
        #contract_type=client.Options.ContractType.ALL)
    assert r.status_code == 200, r.raise_for_status()
    out = r.json()
    with open('call.json', 'w') as f:
        json.dump(out, f, indent=2)
    return out

#gets put options chain
def put_option_chain(client, ticker: str):
    expDate = date.today() + timedelta(DAYSOUT)

    r = client.get_option_chain(
        symbol=ticker,
        contract_type=client.Options.ContractType.PUT,
        to_date=expDate,
        from_date=date.today(),
        strike_count=CHAINSIZE,
        strategy=client.Options.Strategy.ANALYTICAL
        )
        #contract_type=client.Options.ContractType.ALL)
    assert r.status_code == 200, r.raise_for_status()
    out = r.json()
    with open('put.json', 'w') as f:
        json.dump(out, f, indent=2)
    return out

#returns IV for call chain
def getCallIV(call) -> float:
    callStrikes = (call['callExpDateMap'][list(call['callExpDateMap'].keys())[0]].keys())
    listCallStrikes = list(callStrikes)
    listCallVol =[]
    listCalltotVol = []
    listCallopIn = []

    #formatting for option chain
    #print("-----------Call option chain-----------")

    for x in listCallStrikes:
        callvol = call['callExpDateMap'][list(call['callExpDateMap'].keys())[0]][x][0]['volatility']
        calltotVol = call['callExpDateMap'][list(call['callExpDateMap'].keys())[0]][x][0]['totalVolume']
        callopIn = call['callExpDateMap'][list(call['callExpDateMap'].keys())[0]][x][0]['openInterest']

        #code to pring the option chain if you want to see it
        #print(json.dumps(call['callExpDateMap'][list(call['callExpDateMap'].keys())[0]][x][0]['description'],indent = 4) + " " +
        #    str(callvol) + " " + str(calltotVol) + " " + str(callopIn)
        #)

        listCallVol.append(callvol)
        listCalltotVol.append(calltotVol)
        listCallopIn.append(callopIn)

    indexOne = np.argmax(np.array(listCalltotVol))
    indexTwo = np.argmax(np.array(listCallopIn))

    newList = replaceNan(getAvg(listCallVol), listCallVol)

    print('Avg IV for ' + str(CHAINSIZE) + ': ' + str(getAvg(listCallVol)))

    return round(((newList[indexOne] + newList[indexTwo]) / 2), 3)


def getPutIV(put) -> float:
    putStrikes = (put['putExpDateMap'][list(put['putExpDateMap'].keys())[0]].keys())
    listPutStrikes = list(putStrikes)
    listPutVol =[]
    listPuttotVol = []
    listPutopIn = []

    #formatting for option chain
    #print("-----------put option chain-----------")

    for x in listPutStrikes:
        putvol = put['putExpDateMap'][list(put['putExpDateMap'].keys())[0]][x][0]['volatility']
        puttotVol = put['putExpDateMap'][list(put['putExpDateMap'].keys())[0]][x][0]['totalVolume']
        putopIn = put['putExpDateMap'][list(put['putExpDateMap'].keys())[0]][x][0]['openInterest']

        #code to pring the option chain if you want to see it
        #print(json.dumps(put['putExpDateMap'][list(put['putExpDateMap'].keys())[0]][x][0]['description'],indent = 4) + " " +
        #    str(putvol) + " " + str(puttotVol) + " " + str(putopIn)
        #)

        listPutVol.append(putvol)
        listPuttotVol.append(puttotVol)
        listPutopIn.append(putopIn)

    indexOne = np.argmax(np.array(listPuttotVol))
    indexTwo = np.argmax(np.array(listPutopIn))

    newList = replaceNan(getAvg(listPutVol), listPutVol)

    print('Avg IV for ' + str(CHAINSIZE) + ': ' + str(getAvg(listPutVol)))

    return round(((newList[indexOne] + newList[indexTwo]) / 2), 3)

#expected move formula using IV
def expectedRange(volatility, daysToExpiration, stockPrice) -> float:
    sq = math.sqrt(daysToExpiration / 365)
    return round((sq * (volatility/100) * stockPrice), 2)

#returns the avg but should remove the Nan's
def getAvg(l):
    total = 0
    num = 0
    for x in l:
        if x != 'NaN':
            total = total + x
            num = num + 1
    return round((total / num), 3)

#replace the NaN with avg from above
#I cant believe I had to write these functions
def replaceNan(avg, l):
    nl = []
    for x in l:
        if x != 'NaN':
            nl.append(x)
        else:
            nl.append(avg)
    return nl
