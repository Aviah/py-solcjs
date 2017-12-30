import json
import os
import shutil
from solcjs import ASSETS_DIR

from ..utils.filesystem import (
    ensure_path_exists,
)

from .versions import (
    V1,
    LATEST_VERSION,
)

PY_SOLCJS_USER_BASE_PATH = os.path.expanduser('~/.py_solcjs')
PY_SOLCJS_JSON_CONFIG_FILENAME = './config.json'

DEFAULT_V1_CONFIG_FILENAME = "defaults.v1.config.json"
DEFAULT_RELEASES_FILENAME = "solcjs_releases.json"

DEFAULT_COMPILE_SCRIPT_FILENAME = "compile.js"

DEFAULT_CONFIG_FILENAMES = {
    V1: DEFAULT_V1_CONFIG_FILENAME,
}


def get_default_config_path(version=LATEST_VERSION):
    try:
        return os.path.join(ASSETS_DIR, DEFAULT_CONFIG_FILENAMES[version])
    except KeyError:
        raise KeyError(
            "`version` must be one of {0}".format(
                sorted(tuple(DEFAULT_CONFIG_FILENAMES.keys()))
            )
        )


def get_default_releases_path():
    return os.path.join(ASSETS_DIR, DEFAULT_RELEASES_FILENAME)


def get_user_config_path():

    return os.path.join(
        PY_SOLCJS_USER_BASE_PATH,
        PY_SOLCJS_JSON_CONFIG_FILENAME,
    )


def get_default_compile_script_path():
    return os.path.join(ASSETS_DIR, DEFAULT_COMPILE_SCRIPT_FILENAME)


def get_compile_script_path():
    return os.path.join(PY_SOLCJS_USER_BASE_PATH, DEFAULT_COMPILE_SCRIPT_FILENAME)


def load_config(version=LATEST_VERSION):
    user_config_path = get_user_config_path()
    if not os.path.exists(user_config_path):
        ensure_path_exists(PY_SOLCJS_USER_BASE_PATH)
        shutil.copyfile(
            get_default_config_path(),
            user_config_path
        )
        shutil.copyfile(
            get_default_releases_path(),
            os.path.join(PY_SOLCJS_USER_BASE_PATH, DEFAULT_RELEASES_FILENAME)
        )
        shutil.copyfile(
            get_default_compile_script_path(),
            get_compile_script_path()
        )
    with open(user_config_path) as config_file:
        config = json.load(config_file)
    return config
