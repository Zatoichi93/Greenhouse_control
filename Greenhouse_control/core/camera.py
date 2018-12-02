from picamera import PiCamera
import picamera
import deepzoom
import datetime
import shutil

class Camera:

    def __init__(self, path, logging):
        self.log = logging
        self.path = path
        self.camera = PiCamera()
        self.camera.resolution = (2592, 1944)

    def take(self, photo_name):
        self.log.debug("Take a photo")
        self.camera.capture(self.path+photo_name)

    def snapshot(self):
        self.log.debug("Take a snapshot")
        self.camera.annotate_text_size = 120
        self.camera.annotate_background = picamera.Color('black')
        self.camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.camera.capture(self.path+"snapshot.png")
        shutil.rmtree(self.path+"snapshot_files", ignore_errors=True)
        self.log.debug("Make the snapshot zoomable")
        deepzoom.ImageCreator().create(self.path+"snapshot.png", self.path+"snapshot.dzi")

    def close(self):
        self.camera.close()

