import os
import sys


def get_config_path(user_conf):
    expanded_path = os.path.expanduser(user_conf)
    if os.path.exists(expanded_path):
        return expanded_path
    if user_conf != "~/.datasets":
        print("Config file {} does not exist".format(user_conf))
        sys.exit(1)
    else:
        return
