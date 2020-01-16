import requests
import json
import datetime
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('actualcredentials.json', scope)
client = gspread.authorize(creds)
if __name__ == '__main__':
    while True:
        if (time.time().__round__() % 60 == 0):
            data = []
            sheet = client.open("PriceData").sheet1
            api = requests.get("https://www.predictit.org/api/marketdata/all/").json()
            for i in api['markets']:
                if i['name'].find('@realDonaldTrump') != -1:
                    tweetURL = "https://www.predictit.org/api/marketdata/markets/" + str(i['id'])
            tweet = requests.get(tweetURL).json()
            data.append(datetime.datetime.now().strftime("%H"))
            data.append(datetime.datetime.now().strftime("%M"))
            data.append(str(datetime.datetime.now().weekday()))
            for i in tweet['contracts']:
                data.append(str(i['lastTradePrice']))
            sheet.update_cell(1, 1, int(sheet.cell(1, 1).value) + 1)
            sheet.insert_row(data, int(sheet.cell(1, 1).value))
        time.sleep(1)
