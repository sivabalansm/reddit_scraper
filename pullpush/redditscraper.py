#! /bin/python3
import requests
import json
from datetime import datetime, timedelta



BASEURL = 'https://api.pullpush.io/reddit/search/'

class redditScraper:
    def __init__(self, directory: str):
        self.directory = directory + "/?"
        self.searchParams = []

    def __addParam(self, param: str):
        self.searchParams.append(param)

    def setSub(self, sub: str):
        self.__addParam(f"subreddit={sub}")

    def setSize(self, size: int):
        self.__addParam(f"size={size}")

    def setBefore(self, epoch):
        self.__addParam(f"before={epoch}")
    
    def setAfter(self, epoch):
        self.__addParam(f"after={epoch}")

    def setAuthor(self, author: str):
        self.__addParam(f"author={author}")

    def scrape(self):
        fullStringParams = '&'.join(self.searchParams)
        return json.loads(requests.get(BASEURL + self.directory + fullStringParams).text)





class redditParser:
    def __init__(self, jsonData: dict):
        self.dataList = jsonData['data']

    def __len__(self):
        return len(self.dataList)
    
    def getTimes(self, humanReadable=True):
        if not humanReadable:
            return [int(dataEntry['created_utc']) for dataEntry in self.dataList]
        return [(datetime.fromtimestamp(dataEntry['created_utc'])).strftime('%Y-%m-%d %I:%M:%S %P') for dataEntry in self.dataList]
    
    def getLatestTS(self):
        return int(self.getTimes(humanReadable=False)[0])

    def getOldestTS(self):
        return int(self.getTimes(humanReadable=False)[-1])

    def getUsers(self):
        return [dataEntry['author'] for dataEntry in self.dataList]

    def getSubs(self):
        return [dataEntry['subreddit'] for dataEntry in self.dataList]

    def getText(self):
        if 'body' in self.dataList[0]:
            return [dataEntry['body'] for dataEntry in self.dataList]
        else:
            return [(dataEntry['title'], dataEntry['selftext']) for dataEntry in self.dataList]
    def getParams(self):
        return [param for param in self.dataList[0]]








