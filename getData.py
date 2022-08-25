from tda import auth, client
from webdriver_manager.chrome import ChromeDriverManager
from auth_params import ACCT, API, CALLBACK
from selenium import webdriver

from datetime import date, timedelta

import json

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
    expDate = date.today() + timedelta(3)
    #strike_range=client.Options.StrikeRange.NEAR_THE_MONEY, if you want NTM
    r = client.get_option_chain(
        symbol=ticker,
        contract_type=client.Options.ContractType.CALL,
        to_date=expDate,
        strike_count=20
        )
        #contract_type=client.Options.ContractType.ALL)
    assert r.status_code == 200, r.raise_for_status()
    out = r.json()
    with open('call.json', 'w') as f:
        json.dump(out, f, indent=2)
    return out

def put_option_chain(client, ticker: str):
    r = client.get_option_chain(
        symbol=ticker,
        contract_type=client.Options.ContractType.PUT,
        strike_range=client.Options.StrikeRange.NEAR_THE_MONEY,
        days_to_expiration=2
        )
        #contract_type=client.Options.ContractType.ALL)
    assert r.status_code == 200, r.raise_for_status()
    out = r.json()
    with open('put.json', 'w') as f:
        json.dump(out, f, indent=2)
    return out
