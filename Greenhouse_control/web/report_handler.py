import tornado.web
import datetime
import bson.json_util


class ReportHandler(tornado.web.RequestHandler):

    def initialize(self, co):
        self.core = co

    def get(self):
        self.render("reports.html")

    def post(self):
        _id = {}
        fromDate = datetime.datetime.strptime(self.get_argument("fromDate"), "%d/%m/%Y")
        toDate = datetime.datetime.strptime(self.get_argument("toDate"), "%d/%m/%Y")
        timespan = self.get_argument("timespan")
        if timespan == 1:
            _id = {"day": {"$dayOfYear": "$date"}}
        if timespan == 7:
            _id = {"week": {"week": "$date"}}
        if timespan == 30:
            _id = {"month": {"$dayOfYear": "$date"}}

        pipeline = [{
            '$match': {
                'date': {
                    '$gt': fromDate,
                    '$lt': toDate
                }
            }
            }, {
            '$group': {
                '_id': {
                    'year': {'$year': '$date'},
                    'month': {'$month': '$date'},
                    'day': {'$dayOfMonth': '$date'},
                    'week': {'$week': '$date'}
                },
                'avgTemperature': {'$avg': '$temperature'},
                'avgHumidity': {'$avg': '$humidity'},
                'total': {'$sum': '$total_time'},
                'heat': {'$sum': '$heat_time'}
                }
            }
        ]
        res = self.core.db.command('aggregate', 'env', pipeline=pipeline, explain=True)
        #res = self.core.collection.aggregate(pipeline)

        self.write(bson.json_util.dumps(res))
