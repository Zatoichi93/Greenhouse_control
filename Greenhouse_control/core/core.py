from pymongo import MongoClient
from bson import json_util
import serial
import logging
from camera import Camera
import datetime
from config import Config
from wrapper import Wrapper
from music import Music
import threading
import os.path
from time import sleep

class Core:
    def __init__(self, debug):
        level = logging.DEBUG if debug else logging.WARNING

        self.cfg = Config('core/config.json')
        logging.basicConfig(filename='logs/'+datetime.datetime.now().strftime('%y%m%d%H%m%s')+'.log',
                            filemode="w",
                            format='%(levelname)s: %(asctime)s %(message)s',
                            level=level)
        self.com = serial.Serial(self.cfg.serialport(), self.cfg.baudrate())
        self.wrap = Wrapper(self.cfg, self.com, logging)
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[self.cfg.database()]
        self.collection = self.db[self.cfg.collection()]
        logging.debug("Connected to database")
        self.cam = Camera(self.cfg.photopath(), logging)
        self.music = Music(self.cfg.music_dir())
        self.on = False
        self.changed = True

    def __camera(self):
        return self.cam

    def __dbcollection(self):
        return self.collection

    def __wrapper(self):
        return self.wrap

    def __config(self):
        return self.cfg

    camera = property(__camera)
    dbcollection = property(__dbcollection)
    wrapper = property(__wrapper)
    config = property(__config)

    def __read(self):
        data = self.wrap.read()
        if data is not None:
            try:
                bson_data = json_util.loads(data)
                bson_data['date'] = datetime.datetime.now()
                bson_data['temperature'] = bson_data.pop('t')
                bson_data['humidity'] = bson_data.pop('h')
                bson_data['soil'] = bson_data.pop('s')
                bson_data['light'] = bson_data.pop('l')
                bson_data['total_time'] = bson_data.pop('tt')
                bson_data['heat_time'] = bson_data.pop('ht')
                logging.debug(bson_data)
                i = self.collection.insert_one(bson_data).inserted_id
                logging.debug("New record set with id: "+str(i))
            except ValueError:
                logging.warning("Invalid json, message get was: "+str(data))
        threading.Timer(30, self.__read).start()

    def __shot(self):
        photo_name = datetime.datetime.now().strftime('%y%m%d_%H')+".png"
        if not os.path.isfile(self.cfg.photopath()+photo_name):
            self.on = True
            self.wrap.light(self.on)
            sleep(2)
            self.camera.take(photo_name)
        threading.Timer(20, self.__shot).start()

    def __light(self):
        end_hour = self.cfg.light_start() + self.cfg.light_hours() - 24
        start_hour = self.cfg.light_start()
        logging.debug("Light will be on from " + str(start_hour)
                      + " to " + str(end_hour)
                      + " now are " + str(datetime.datetime.now().hour))
        now = datetime.datetime.now()
        if now.hour >= start_hour or now.hour <= end_hour:
            self.changed = True if not self.on else False
            self.on = True
        else:
            self.changed = True if self.on else False
            self.on = False

        if self.changed:
            self.wrap.light(self.on)
        threading.Timer(40, self.__light).start()

    def __play(self):
        self.music.play()

    def start(self):
        try:
            threading.Timer(30, self.__read).start()
            threading.Timer(40, self.__shot).start()
            threading.Timer(20, self.__light).start()
            threading.Thread(target=self.__play).start()
        except KeyboardInterrupt:
            self.cam.close()
        except Exception:
            os.system('reboot')

