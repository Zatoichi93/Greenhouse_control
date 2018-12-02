import json


class Config:

    def __init__(self, path):
        self.path = path
        with open(path) as json_data_file:
            self.config_data = json.load(json_data_file)

    def __save(self):
        with open(self.path, 'w') as json_file:
            json.dump(self.config_data, json_file)

    def serialport(self, port=None):
        res = self.config_data["serial_port"]
        if port is not None:
            self.config_data["serial_port"] = port
            self.__save()
        return res

    def baudrate(self, baudrate=None):
        res = self.config_data["baud_rate"]
        if baudrate is not None:
            self.config_data["baud_rate"] = int(baudrate)
            self.__save()
        return res


    def photopath(self, photo_path=None):
        res = self.config_data["image_dir"]
        if photo_path is not None:
            self.config_data["image_dir"] = photo_path
            self.__save()
        return res

    def light_hours(self, light_hours=None):
        res = self.config_data["light_hours"]
        if light_hours is not None:
            self.config_data["light_hours"] = int(light_hours)
            self.__save()
        return res

    def light_start(self, light_start=None):
        res = self.config_data["start_light_hour"]
        if light_start is not None:
            self.config_data["start_light_hour"] = int(light_start)
            self.__save()
        return res

    def database(self):
        res = self.config_data["database_name"]
        return res

    def collection(self):
        res = self.config_data["collection_name"]
        return res

    def maxTemp(self, max_temp=None):
        res = self.config_data["max_temperature"]
        if max_temp is not None:
            self.config_data["max_temperature"] = int(max_temp)
        return res

    def tgtTemp(self, tgt_temp=None):
        res = self.config_data["tgt_temperature"]
        if tgt_temp is not None:
            self.config_data["tgt_temperature"] = int(tgt_temp)
        return res
