from __future__ import absolute_import

import json
import os
import subprocess

from .exceptions import (
    SolcError,
)

from .config.defaults import (
    get_compile_script_path,
    load_config,
)

from .utils.string import (
    coerce_return_to_text,
)


def get_solcjs_binary_path():
    return os.environ.get('SOLC_BINARY', 'solcjs')


def get_node_binary_path():
    return os.environ.get('NODE_BINARY', 'node')


def solc_default_version():
    # the node module installed version
    solc_binary = get_solcjs_binary_path()
    command = [solc_binary]
    command.append('--version')

    proc = subprocess.Popen(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    stdoutdata, stderrdata = proc.communicate()

    if proc.returncode != 0:
        raise SolcError(
            command=command,
            return_code=proc.returncode,
            stdout_data=stdoutdata,
            stderr_data=stderrdata,
        )

    return stdoutdata, stderrdata, command, proc


#@coerce_return_to_text
def solc_wrapper(stdin,
                 node_binary=None,
                 compilation_version=None,
                 input_file=None,
                 output_file=None,
                 write_to_files=False,
                 success_return_code=0):

    config = load_config()

    if node_binary is None:
        node_binary = get_node_binary_path()

    command = [node_binary, "-e"]

    with open(get_compile_script_path(), "r") as script_file:
        script = script_file.read()

    if compilation_version:
        script = "version = '{0}';".format(compilation_version) + script

    if write_to_files:
        input_json = input_file or config["inputFile"]
        with open(input_json, "w+") as f:
            json.dump(stdin, f)

    script = "var input_json = {0};".format(json.dumps(stdin)) + script
    command.append(script)

    proc = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if proc.returncode != success_return_code:
        raise SolcError(
            command=command,
            return_code=proc.returncode,
            stdin_data=stdin,
            stdout_data=proc.stdout,
            stderr_data=proc.stderr,
        )

    if write_to_files:
        output_file = output_file or config["outputFile"]
        with open(output_file, "w+") as f:
            f.write(proc.stdout.decode('utf-8'))

    return proc.stdout, proc.stderr, command, proc
