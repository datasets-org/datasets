import requests


class Datasets(object):
    def __init__(self, conf):
        self.conf = conf
        self.address = self.conf["address"]

    def info(self, id, usage={}):
        return requests.post(self.address + "/use/" + id, json=usage).json()
