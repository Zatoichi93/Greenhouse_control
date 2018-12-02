import tornado.web


class MainHandler(tornado.web.RequestHandler):

    def initialize(self, co):
        self.core = co

    def get(self):
        res = self.core.collection.find_one({}, sort=[('date', -1)])
        light = "Accese" if res['light'] else "Spente"
        snapshot = self.core.config.photopath() + "snapshot.png"
        self.render("dashboard.html",
                    title="Greenhouse", snapshot_url=snapshot,
                    temperature=res['temperature'], humidity=res['humidity'],
                    light=light, soil=res['soil'])
