# badBot
python bot for trading using TDA API 

This Bot focuses specifically on Option Trading Spy 
Works using Delta for options with strike expiration set to next available trading day

### Things to Note:
1. You are going to need to make auth_params.py file with the following variables 
> API = "Your API key here"
> ACCT = "Your account number here"
> CALLBACK = "Callback url, if unsure use http://127.0.0.1:8080"

2. Install needed libraries
 - tda 
 - webdriver_manager 
 - selenium 
 - numpy 