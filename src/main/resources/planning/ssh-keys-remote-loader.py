#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from com.xebialabs.deployit.io import ArtifactAwareLocalFile
from com.xebialabs.overthere.local import LocalConnection
from java.io import File


def sshkey_files_container():
    result = []
    for _delta in deltas.deltas:
        deployed = _delta.deployedOrPrevious
        if (_delta.operation == "CREATE" or _delta.operation == "MODIFY") and deployed.type == "ansible.Roles":
            result.append(deployed.container)
    return set(result)


for container in sshkey_files_container():
    context.addStep(steps.jython(
        description="Uploading {0} ssh key to the ansible controller".format(container.name, container.ansibleController.name),
        order=20,
        script="upload_ssk_key.py",
        jython_context={
            "container": container,
            "target_directory": "container.ansibleController.ansibleSShKeyFolder",
            "target_path": "{0}/{1}.pem".format(container.ansibleController.ansibleSShKeyFolder, container.name),
            "target_host": "container.ansibleController.host"}
    ))

    context.addStep(steps.jython(
        description="Delete {0} ssh key from the ansible controller".format(container.name, container.ansibleController.name),
        order=99,
        script="remove_ssk_key.py",
        jython_context={
            "container": container,
            "target_directory": "container.ansibleController.ansibleSShKeyFolder",
            "target_path": "{0}/{1}.pem".format(container.ansibleController.ansibleSShKeyFolder, container.name),
            "target_host": "container.ansibleController.host"}
    ))
