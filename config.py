from os import path as os_path
from yaml import safe_load
from os import getenv


def get_config():
    if getenv("KUBERNETES_PORT_443_TCP_ADDR") is not None:
        config_path = "%s/config/config_prod.yaml" % os_path.split(os_path.realpath(__file__))[0]
    else:
        config_path = "%s/config/config_dev.yaml" % os_path.split(os_path.realpath(__file__))[0]
    with open(config_path, 'r') as CONFIG:
        config = safe_load(CONFIG)
    return config
