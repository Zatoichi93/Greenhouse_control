import json


class Wrapper:

    def __init__(self, cfg, ser, log):
        self.serial = ser
        self.cfg = cfg
        self.log = log

    def read(self):
        self.serial.write("READ\n")
        data = None
        try:
            data = self.serial.readline()
        except Exception:
            self.log.warning("Something appenend when read from serial")
        return data

    def config(self):
        self.serial.write("GET\n")
        data = self.serial.readline()
        if data is not None:
            try:
                json_data = json.loads(data)
                self.log.debug(json_data)
                return json_data
            except ValueError:
                self.log.warning("Il messaggio non era json")

    def light(self, on):
        if on:
            self.serial.write("ON\n")
            self.log.debug("Light turned on")
        else:
            self.serial.write("OFF\n")
            self.log.debug("Light turned off")

    def max(self, value):
        self.serial.write("SET M "+value)
        self.log.debug("Maximum temperature set to: "+value)
        self.cfg.maxTemp(value)

    def target(self, value):
        self.serial.write("SET T "+value)
        self.log.debug("Target temperature set to: "+value)
        self.cfg.tgtTemp(value)
