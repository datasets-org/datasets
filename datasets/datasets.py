import os

import requests
import yaml


def ensure_data(fn):
    def decorator(*args, **kwargs):
        self = args[0]
        if not self.data:
            if "id" in kwargs:
                id = kwargs["id"]
            elif len(args) > 1:
                id = args[1]
            else:
                raise TypeError("Datasets: You have to specify id")

            if "usage" in kwargs:
                self.usage.update(kwargs["usage"])
            elif len(args) > 2:
                self.usage.update(args[2])
            self._load_data(id, usage=self.usage)
        return fn(*args, **kwargs)

    decorator.__name__ = fn.__name__
    return decorator


class Datasets(object):
    def __init__(self, id=None, usage={}, conf={}):
        self.USER_CONF = "~/.datasets"
        self.conf = conf
        self.usage = usage
        if "address" not in conf:
            self._user_server()
        else:
            self.address = self.conf["address"]

        self.data = None
        if id:
            self._load_data(id, usage=usage)

    def _load_data(self, id, usage={}):
        self.data = requests.post(self.address + "/use/" + id, \
                                  json=usage).json()

    def _user_server(self):
        expanded_path = os.path.expanduser(self.USER_CONF)
        if os.path.exists(expanded_path):
            self.address = "http://" + open(expanded_path).read()

    @ensure_data
    def info(self, id=None, usage={}):
        return self.data

    @ensure_data
    def paths(self, id=None, usage={}):
        if "paths" not in self.data:
            raise Exception("Data set has no paths")
        if "data" not in self.data:
            raise Exception("Data set has no data")
        paths = []
        for i in self.data["paths"]:
            for d in self.data["data"]:
                paths.append(os.path.join(i, d))
        return paths

    @ensure_data
    def labeled_paths(self, id=None, usage={}):
        if "labels" not in self.data:
            raise Exception("No labels")
        labels = self.data["labels"]
        pths = self.paths()
        return dict(zip(labels, pths))

    def create(self, data={}, path=None):
        uid = requests.get(self.address + "/new").json()
        requests.post(self.address + "/update/" + uid, json=data)
        if path is not None:
            data.update({"id": uid.encode("utf-8")})
            yaml.dump(data, open(os.path.join(path, "dataset.yaml"), "w"),
                      default_flow_style=False)
        requests.post(self.address + "/reload")
        return uid
