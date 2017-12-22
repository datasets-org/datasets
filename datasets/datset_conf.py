import os
import yaml

DATASET_FILENAME = "dataset.yaml"


def _find_conf():
    while True:
        if os.path.exists(DATASET_FILENAME):
            return open(DATASET_FILENAME)
        os.chdir("..")
    # todo only some hops - then err


def get_ds_id():
    return yaml.load(_find_conf())["id"]
