from core.core import Core
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.process
import os.path
from web import *

DEBUG = False
core = Core(DEBUG)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", main_handler.MainHandler, dict(co=core)),
            (r"/enviroment", enviromentdata_handler.EnviromentDataHandler, dict(co=core)),
            (r"/shot", PhotoHandler),
            (r"/settings", SettingsHandler),
            (r"/power", powerdata_handler.PowerDataHandler, dict(co=core)),
            (r"/charts", ChartsHandler),
            (r"/reports", report_handler.ReportHandler, dict(co=core))
        ]
        settings = dict(
            debug=DEBUG,
            cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)



class PhotoHandler(tornado.web.RequestHandler):
    def get(self):
        core.camera.snapshot()

class SettingsHandler(tornado.web.RequestHandler):
    def get(self):
        maxTemp = core.config.maxTemp()
        targetTemp = core.config.tgtTemp()
        ligt_start = core.config.light_start()
        light_hours = core.config.light_hours()
        self.render("settings.html", title="Greenhouse",
                    max_temp=maxTemp, tgt_temp=targetTemp,
                    light_start=ligt_start, light_hours=light_hours)

    def post(self):
        maxT = self.get_argument('maxTemperature')
        tgtT = self.get_argument('targetTemperature')
        hours = self.get_argument('lightHours')
        start = self.get_argument('startHour')
        core.config.maxTemp(maxT)
        core.wrapper.max(str(maxT))
        core.config.tgtTemp(tgtT)
        core.wrapper.target(str(tgtT))

        core.config.light_hours(hours)
        core.config.light_start(start)


class ChartsHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("charts.html", title="Greenhouse")


if __name__ == "__main__":
    core.start()
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

