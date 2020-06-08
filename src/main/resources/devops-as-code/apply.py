#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from overtherepy import LocalConnectionOptions, OverthereHost, OverthereHostSession
from com.xebialabs.overthere import OperatingSystemFamily
from com.xebialabs.overthere.util import OverthereUtils
from java.nio.charset import Charset
from java.lang import System


ansible_controler = repositoryService.read(ansible_controller_id)

remote_session = OverthereHostSession(ansibleController.host)
remote_yaml_file = remote_session.remote_file(yaml_file)
print("remote_yaml_file {0}".format(remote_yaml_file))

operating_system = System.getProperty("os.name").lower()
print(operating_system)
if operating_system.startswith("win"):
    os = OperatingSystemFamily.WINDOWS
else:
    os = OperatingSystemFamily.UNIX

local_opts = LocalConnectionOptions(os=os)
local_host = OverthereHost(local_opts)
local_session = OverthereHostSession(local_host)
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
           }

command_line = "/usr/local/bin/xl --xl-deploy-password {devopsAsCodePassword} --xl-deploy-username {devopsAsCodeUsername} --xl-deploy-url {devopsAsCodeUrl} apply  -f {yaml_file}".format(**context)
print(command_line)
response = local_session.execute(command_line)
