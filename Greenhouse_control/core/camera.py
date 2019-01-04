from picamera import PiCamera
import picamera
import deepzoom
import datetime
import shutil
from time import sleep

class Camera:

    VFLIP = True
    HFLIP = True
    HRES = 3280
    VRES = 2464

    def __init__(self, path, logging):
        self.log = logging
        self.path = path
        #self.camera = PiCamera()
        #self.camera.vflip = self.VFLIP
        #self.camera.hflip = self.HFLIP
        #self.camera.resolution = (self.HRES, self.VRES)

    def take(self, photo_name):
        camera = PiCamera()
        camera.vflip = self.VFLIP
        camera.hflip = self.HFLIP
        camera.resolution = (self.HRES, self.VRES)
        self.log.debug("Take a photo")
        camera.shutter_speed = 10000
        camera.capture(self.path+photo_name)
        camera.close()

    def snapshot(self):
        camera = PiCamera()
        camera.vflip = self.VFLIP
        camera.hflip = self.HFLIP
        camera.resolution = (self.HRES/2, self.VRES/2)
        log.debug("Take a snapshot")
        camera.annotate_text_size = 120
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.capture(self.path+"snapshot.png")
        camera.close()
        shutil.rmtree(self.path+"snapshot_files", ignore_errors=True)
        self.log.debug("Make the snapshot zoomable")
        deepzoom.ImageCreator().create(self.path+"snapshot.png", self.path+"snapshot.dzi")

    def close(self):
        self.camera.close()

