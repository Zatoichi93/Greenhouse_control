import tornado.web
import json


class PowerDataHandler(tornado.web.RequestHandler):

    def initialize(self, co):
        self.core = co

    def get(self):
        result =self.core.collection.aggregate([
            {"$group": {
                "_id": "null",
                "totalTime": {"$sum": "$total_time"},
                "heatTime": {"$sum": "$heat_time"}
            }}
        ])
        dic =[]
        for s in result:
            onPercentage = (s['heatTime']/s['totalTime'])*100
            dic.append(dict(status='off', time=100-onPercentage))
            dic.append(dict(status='on', time=onPercentage))

        self.write(json.dumps(dic))
