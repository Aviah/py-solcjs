import os


def ensure_path_exists(dir_path):
    """
    Make sure that a path exists
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        return True
    return False


def is_executable_available(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath = os.path.dirname(program)
    if fpath:
        if is_exe(program):
            return True
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return True

    return False
