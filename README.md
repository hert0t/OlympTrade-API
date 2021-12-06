## REQUIREDMENT ##
- ACCOUNT SESSION ID (YOU CAN GET BY INSPECT OLYMPTRADE FROM CHROME/FIREFOX IN: wss://olymptrade.com/ds/v6)
- GERMAN VPS ( FAST SPEED )

## EXAMPLE USAGE ##
- BET BUY/SELL
```PY
from lib import Client
client = Client()
status = client.getBet(status="up",
              pair="EURUSD",
              amount="1",
              duration="60")
print(status)

# STATUS: 'up' for buy, 'down' for sell.
# PAIR: pair currency (u can get list by getCurrency funct).
# AMOUNT: amount bet.
# DURATION: duration bet (in second).
```
