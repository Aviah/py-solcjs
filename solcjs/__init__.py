from __future__ import absolute_import

import os
import sys
import warnings

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

from .main import (  # noqa: F401
    get_solc_version_string,
    get_solc_version,
    compile_files,
    compile_source,
    compile_standard,
    link_code,
)
from .install import (  # noqa: F401
    install_solc,
)
if sys.version_info.major < 3:
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn(DeprecationWarning(
        "The `py-solc` library is dropping support for Python 2.  Upgrade to Python 3."
    ))
    warnings.resetwarnings()
