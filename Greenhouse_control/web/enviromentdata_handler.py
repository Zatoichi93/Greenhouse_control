import tornado.web
import datetime
import json


class EnviromentDataHandler(tornado.web.RequestHandler):
    def initialize(self, co):
        self.core = co

    def get(self):
        older = datetime.datetime.now()-datetime.timedelta(hours=2)
        dic = []
        for s in self.core.dbcollection.find({'date': {'$gt': older, '$lt': datetime.datetime.now()}}).sort('date', -1):

            d = dict(date=s['date'].isoformat(),
                     temperature=s['temperature'],
                     humidity=s['humidity'],
                     soil=s['soil'], light=s['light'])
            dic.append(d)
        res = json.dumps(dic)
        self.write(res)
