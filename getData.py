from tda import auth, client
from webdriver_manager.chrome import ChromeDriverManager
from auth_params import ACCT, API, CALLBACK
from selenium import webdriver

import numpy as np

from datetime import date, timedelta

import json

CHAINSIZE = 30
DAYSOUT = 2

def authenticate():
    token_path = 'aaah.json'
    try:
        client = auth.client_from_token_file(token_path, API)
    except FileNotFoundError:
        with webdriver.Chrome(ChromeDriverManager().install()) as driver:
            client = auth.client_from_login_flow(
                driver, API, CALLBACK, token_path)
    return client

def getprice(client, ticker: str):
    r = client.get_quote(ticker)
    assert r.status_code == 200, r.raise_for_status()

    y = r.json()
    price = y[ticker]["lastPrice"]
    return price

def get_position(client):
    r = client.get_account(ACCT, fields=client.Account.Fields.POSITIONS)
    assert r.status_code == 200, r.raise_for_status()

    out = r.json()

    if "positions" in out["securitiesAccount"]:
        return True
    else:
        return False

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

def getCallIV(call) -> float:
    callStrikes = (call['callExpDateMap'][list(call['callExpDateMap'].keys())[0]].keys())
    #print(callStrikes)
    listCallStrikes = list(callStrikes)
    listCallVol =[]
    listCalltotVol = []
    listCallopIn = []

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

    return round(((newList[indexOne] + newList[indexTwo]) / 2), 3)

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
