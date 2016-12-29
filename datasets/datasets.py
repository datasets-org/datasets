import requests
import os
import yaml


class Datasets(object):
    def __init__(self, conf={}):
        self.USER_CONF = "~/.datasets"
        self.conf = conf
        if "address" not in conf:
            self._user_server()
        else:
            self.address = self.conf["address"]

    def _user_server(self):
        expanded_path = os.path.expanduser(self.USER_CONF)
        if os.path.exists(expanded_path):
            self.address = open(expanded_path).read()

    def info(self, id, usage={}):
        return requests.post(self.address + "/use/" + id, json=usage).json()

    def paths(self, id, usage={}):
        if "action" not in usage:
            usage["action"] = "load"
        data = requests.post(self.address + "/use/" + id, json=usage).json()
        paths = []
        for i in data["paths"]:
            for d in data["data"]:
                paths.append(os.path.join(i, d))
        return paths

    def create(self, data={}, path=None):
        uid = requests.get(self.address + "/new").json()
        requests.post(self.address + "/update/" + uid, json=data)
        if path is not None:
            data.update({"id": uid.encode("utf-8")})
            yaml.dump(data, open(os.path.join(path, "dataset.yaml"), "w"),
                      default_flow_style=False)
        requests.post(self.address + "/reload")
        return uid
