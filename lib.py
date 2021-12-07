from websocket import create_connection
import time, random, string, json, requests, datetime, threading

class Client():
    def __init__(self, session):
        self.headers = {'Cookie': 'session='+session, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
        self.host_v6 = "wss://olymptrade.com/ds/v6"
        self.parsedCurrency = {}
        for wallet in self.getWallet():
            print("Balance: "+str(wallet["amount"])+"USD")
            opt = input("Y/N? ")
            if opt.lower() == "y":self.accountId = str(wallet["account_id"]);self.accountGroup = wallet["group"];break
        self.updateCurrency()

    def generateUuid(self):
        return ''.join([random.choice(string.ascii_uppercase+string.digits) for n in range(18)])

    def getBet(self, status, pair, amount="1", duration="60"):
        ws = create_connection(self.host_v6,header=self.headers)
        ws.send('[{"t":2,"e":23,"uuid":"'+self.generateUuid()+'","d":[{"amount":'+amount+',"dir":"'+status+'","pair":"'+pair+'","cat":"'+self.parsedCurrency[pair]+'","pos":0,"source":"platform","account_id":'+self.accountId+',"group":"'+self.accountGroup+'","timestamp":'+str(int(time.time()))+',"risk_free_id":null,"duration":'+duration+'}]}]')
        data =  json.loads(ws.recv())
        ws.close()
        return data[0]["d"][0]

    def getWallet(self):
        ws = create_connection(self.host_v6,header=self.headers)
        ws.send('[{"t":2,"e":98,"uuid":"'+self.generateUuid()+'","d":[54]}]')
        data = json.loads(ws.recv())
        ws.close()
        return data[0]["d"]

    def getBalance(self):
        data = self.getWallet()
        return [i["amount"] for i in data if str(i["account_id"]) == self.accountId][0]

    def getOngoingBet(self):
        ws = create_connection(self.host_v6,header=self.headers)
        ws.send('[{"t":2,"e":31,"uuid":"'+self.generateUuid()+'","d":[{"account_id":'+self.accountId+',"group":"'+self.accountGroup+'"}]}]')
        data =  json.loads(ws.recv())[0]["d"]
        ws.close()
        return data

    def getCurrency(self):
        ws = create_connection(self.host_v6,header=self.headers)
        ws.send('[{"t":2,"e":98,"uuid":"'+self.generateUuid()+'","d":[70]}]')
        ws.recv()
        data = json.loads(ws.recv())[0]["d"]
        ws.close()
        return data

    def getHistory(self):
        headers = {**self.headers.copy(), **{'X-App-Version': '7673', 'X-Request-Project': 'bo', 'X-Request-Type': 'Api-Request', 'X-Requested-With': 'XMLHttpRequest'}}
        data = {"limit": 10, "group": self.accountGroup, "order": "time_close", "page": 1, "account_id": int(self.accountId)}
        return requests.post("https://api.olymptrade.com/v3/cabinet/deals-history",headers=headers,json=data).json()

    def updateCurrency(self):
        ws = create_connection(self.host_v6,header=self.headers)
        ws.send('[{"t":2,"e":98,"uuid":"'+self.generateUuid()+'","d":[70]}]')
        ws.recv()
        data = json.loads(ws.recv())[0]["d"]
        ws.close()
        for i in data:self.parsedCurrency[i["name"]] = i["group"]
