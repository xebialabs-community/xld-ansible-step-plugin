#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from overtherepy import LocalConnectionOptions, OverthereHost, OverthereHostSession, StringUtils, BashScriptBuilder, CommandResponse, SshConnectionOptions
from com.xebialabs.overtherepy import PyLoggerExecutionOutputHandler
from com.xebialabs.overthere import OperatingSystemFamily
from com.xebialabs.overthere.util import OverthereUtils, MultipleOverthereExecutionOutputHandler, CapturingOverthereExecutionOutputHandler
from java.nio.charset import Charset
from java.lang import System
from com.xebialabs.overthere import CmdLine
import time
import sys


def local_execute(session, cmd):
    """
    Executes the command on the remote system and returns the result
    :param session: checks the return code is 0. On failure the output is printed to stdout and a system exit is performed
    :param cmd: Command line as an Array of Strings or String.  A String is split by space.
    :return: CommandResponse
    """
    if isinstance(cmd, basestring):
        cmd = cmd.split()

    cmdline = CmdLine.build(cmd)
    capture_so_handler = CapturingOverthereExecutionOutputHandler.capturingHandler()
    capture_se_handler = CapturingOverthereExecutionOutputHandler.capturingHandler()

    console_so_handler = PyLoggerExecutionOutputHandler.sysoutHandler(session.logger)
    console_se_handler = PyLoggerExecutionOutputHandler.syserrHandler(session.logger)
    so_handler = MultipleOverthereExecutionOutputHandler.multiHandler([capture_so_handler, console_so_handler])
    se_handler = MultipleOverthereExecutionOutputHandler.multiHandler([capture_se_handler, console_se_handler])

    rc = session.get_conn().execute(so_handler, se_handler, cmdline)
    # wait for output to drain
    time.sleep(1)

    response = CommandResponse(rc=rc, stdout=capture_so_handler.outputLines, stderr=capture_se_handler.outputLines)

    if response.rc != 0:
        session.logger.error(StringUtils.concat(response.stdout))
        session.logger.error(StringUtils.concat(response.stderr))
        session.logger.error("Exit code {0}".format(response.rc))
        sys.exit(response.rc)
    return response


ansible_controler = repositoryService.read(ansible_controller_id)

remote_session = OverthereHostSession(ansibleController.host)
remote_yaml_file = remote_session.remote_file(yaml_file)
print("remote_yaml_file {0}".format(remote_yaml_file))

operating_system = System.getProperty("os.name").lower()
print("running " + operating_system + " OS on localhost")
if operating_system.startswith("win"):
    os = OperatingSystemFamily.WINDOWS
else:
    os = OperatingSystemFamily.UNIX

local_opts = LocalConnectionOptions(os=os)
local_host = OverthereHost(local_opts)
local_session = OverthereHostSession(local_host, stream_command_output=True)

local_yaml_file = local_session.work_dir_file(remote_yaml_file.getName())
print("local_yaml_file {0}".format(local_yaml_file))

print("copy....")
local_session.copy_to(remote_yaml_file, local_yaml_file)

print("---- YAML ")
print(OverthereUtils.read(local_yaml_file, Charset.defaultCharset().name()))
print("/----")

context = {'devopsAsCodePassword': ansible_controler.devopsAsCodePassword,
           'devopsAsCodeUsername': ansible_controler.devopsAsCodeUsername,
           'devopsAsCodeUrl': ansible_controler.devopsAsCodeUrl,
           'yaml_file': local_yaml_file.path,
           'xlPath': ansible_controler.xlPath
           }

command_line = "{xlPath} --xl-deploy-password {devopsAsCodePassword} --xl-deploy-username {devopsAsCodeUsername} --xl-deploy-url {devopsAsCodeUrl} apply -f {yaml_file} ".format(**context)
print(command_line)

import subprocess

process = subprocess.Popen(command_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
process.wait()
if process.returncode != 0:
    for line in process.stdout:
        local_session.logger.error(line)
    for line in process.stderr:
        local_session.logger.error(line)
    local_session.logger.error("Exit code {0}".format(process.returncode))
    sys.exit(process.returncode)
else:
    for line in process.stdout:
        local_session.logger.info(line)
    for line in process.stderr:
        local_session.logger.info(line)
