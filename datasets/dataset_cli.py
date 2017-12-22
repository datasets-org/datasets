import argparse
import os
import pprint
import sys

import requests
import six
import yaml
from six.moves import input

from datasets_lib import Datasets
from datasets_lib import DatasetsConfig

from confobj import ConfigYaml
from confobj import ConfigEnv
from confobj import ConfigDict

from .utils import get_config_path
from .datset_conf import get_ds_id
from .datset_conf import DATASET_FILENAME


def _get_info(ds):
    return ds.project_details(get_ds_id())


def generate(ds, force=False):
    if not force and os.path.exists(DATASET_FILENAME):
        print("File exists, not overwriting without --force")
        sys.exit(1)
    uid = ds.new()  # todo is it really uid?
    yaml.dump({
        "id": uid,
        "name": "",
        "maintainer": "",
        "data": [''],
        "tags": [''],
    }, open(DATASET_FILENAME, "w"), default_flow_style=False)
    print("dataset.yaml file created")
    print("go ahead and edit it")


def usages(ds):
    pprint.pprint(_get_info(ds)["usages"])


def changelog(ds):
    pprint.pprint(_get_info(ds)["changelog"])


def info(ds):
    pprint.pprint(_get_info(ds))


def scan(ds):
    requests.get(ds.scan())


def config():
    server = input("Server address (example.com): ")
    port = input("Port: ")
    if not six.u(port).isdecimal():
        raise Exception("Port should be numeric")
    # todo
    with open(os.path.expanduser(USER_CONF), "w") as f:
        f.write(server + ":" + port)
    # todo merge yaml


def main():
    parser = argparse.ArgumentParser(description='Dataset CLI')
    parser.add_argument("-s", '--server', dest="server", action='store',
                        help="server")
    parser.add_argument("-c", "--conf", help="config path",
                        default="~/.datasets")
    subparsers = parser.add_subparsers(dest="cmd", help='operation')
    new_p = subparsers.add_parser("new")
    new_p.add_argument("-f", '--force', action='store_true', help="overwrite")
    info_p = subparsers.add_parser("info")
    usages_p = subparsers.add_parser("usages")
    scan_p = subparsers.add_parser("scan")
    config_p = subparsers.add_parser("config")
    changes_p = subparsers.add_parser("changelog")
    args = parser.parse_args()

    conf_path = get_config_path(args.conf)
    dict_conf = ConfigDict({})
    if args.server:
        dict_conf = ConfigDict({
            "host": args.server
        })
    if conf_path:
        config_order = (ConfigYaml(conf_path), ConfigEnv(), dict_conf)
    else:
        config_order = (ConfigEnv(), dict_conf)
    ds_cfg = DatasetsConfig(order=config_order)
    ds = Datasets(conf=ds_cfg)
    if args.cmd == "new":
        generate(ds, args.force)
    if args.cmd == "info":
        info(ds)
    if args.cmd == "usages":
        usages(ds)
    if args.cmd == "scan":
        scan(ds)
    if args.cmd == "config":
        config()
    if args.cmd == "changelog":
        changelog(ds)


if __name__ == "__main__":
    main()
