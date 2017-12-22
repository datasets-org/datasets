import os
import yaml


def _find_conf():
    while True:
        if os.path.exists("dataset.yaml"):
            return open("dataset.yaml")
        os.chdir("..")
    # todo only some hops - then err


def get_ds_id():
    return yaml.load(_find_conf())["id"]
