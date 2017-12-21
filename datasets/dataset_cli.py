import argparse
import os
import pprint
import sys

import requests
import six
import yaml
from six.moves import input

USER_CONF = "~/.datasets"

PROTOCOL = "http://"
server = "localhost:5000"


def _find_conf():
    while True:
        if os.path.exists("dataset.yaml"):
            return open("dataset.yaml")
        os.chdir("..")


def _get_id():
    return yaml.load(_find_conf())["id"]


def _get_info():
    uid = _get_id()
    return requests.get(_get_server() + "detail/" + uid).json()


def _user_server():
    expanded_path = os.path.expanduser(USER_CONF)
    if os.path.exists(expanded_path):
        global server
        server = open(expanded_path).read()


def _get_server():
    return PROTOCOL + server.strip() + "/"


def generate(force=False):
    if not force and os.path.exists("dataset.yaml"):
        print("File exists, not overwriting without --force")
        sys.exit(1)
    uid = requests.get(_get_server() + "new").json()
    yaml.dump({
        "id": uid,
        "name": "",
        "maintainer": "",
        "data": [''],
        "tags": [''],
    }, open("dataset.yaml", "w"), default_flow_style=False)
    print("dataset.yaml file created")
    print("go ahead and edit it")


def usages():
    pprint.pprint(_get_info()["usages"])


def changelog():
    pprint.pprint(_get_info()["changelog"])


def info():
    pprint.pprint(_get_info())


def scan():
    requests.get(_get_server() + "scan")


def config():
    server = input("Server address (example.com): ")
    port = input("Port: ")
    if not six.u(port).isdecimal():
        raise Exception("Port should be numeric")
    with open(os.path.expanduser(USER_CONF), "w") as f:
        f.write(server + ":" + port)


def main():
    parser = argparse.ArgumentParser(description='Dataset CLI')
    parser.add_argument("-s", '--server', dest="server", action='store',
                        help="server")
    subparsers = parser.add_subparsers(dest="cmd", help='operation')
    new_p = subparsers.add_parser("new")
    new_p.add_argument("-f", '--force', action='store_true', help="overwrite")
    info_p = subparsers.add_parser("info")
    usages_p = subparsers.add_parser("usages")
    scan_p = subparsers.add_parser("scan")
    config_p = subparsers.add_parser("config")
    changes_p = subparsers.add_parser("changelog")
    args = parser.parse_args()
    _user_server()
    if args.server:
        global server
        server = args.server
    if args.cmd == "new":
        generate(args.force)
    if args.cmd == "info":
        info()
    if args.cmd == "usages":
        usages()
    if args.cmd == "scan":
        scan()
    if args.cmd == "config":
        config()
    if args.cmd == "changelog":
        changelog()


if __name__ == "__main__":
    main()
