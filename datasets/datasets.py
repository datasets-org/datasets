import os

import requests
import yaml
from confobj import ConfigDict
from confobj import ConfigEnv
from confobj import ConfigYaml
from datasets_lib import Datasets as DatasetsLib
from datasets_lib import DatasetsConfig

from .utils import get_config_path


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
    def __init__(self, id=None, usage={}, conf={}, conf_path="~/.datasets"):
        conf_path_exp = get_config_path(conf_path)
        dict_conf = ConfigDict(conf)
        if conf_path_exp:
            config_order = (ConfigYaml(conf_path_exp), ConfigEnv(), dict_conf)
        else:
            config_order = (ConfigEnv(), dict_conf)
        ds_cfg = DatasetsConfig(order=config_order)
        self.usage = usage
        self._ds = DatasetsLib(conf=ds_cfg)
        self.data = None
        if id:
            self._load_data(id, usage=usage)

    def _load_data(self, ds, id, usage={}):
        self.data = self._ds.use(id, usage)

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
        uid = self._ds.new()
        self._ds.update(uid, data)
        if path is not None:
            data.update({"id": uid.encode("utf-8")})
            yaml.dump(data, open(os.path.join(path, "dataset.yaml"), "w"),
                      default_flow_style=False)
        self._ds.reload()
        return uid
