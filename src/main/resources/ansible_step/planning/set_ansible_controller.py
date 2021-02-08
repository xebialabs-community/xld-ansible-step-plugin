#
# Copyright 2021 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import com.xebialabs.deployit.plugin.api.reflect.Type as Type


def targeted_hosts(deltas):
    result = []
    for _delta in deltas:
        deployed = _delta.deployedOrPrevious
        if deployed.type == "ansible.Roles":
            result.append(deployed.container)
    return set(result)


def default_ansible_controller(default_ansible_controller_id):
    result = repositoryService.query(Type.valueOf('ansible.Controller'), None, None, default_ansible_controller_id, None, None, 0, -1)
    if len(result) == 0:
        return None
    else:
        return repositoryService.read(result[0].id)


default_ansible_controller_id = 'defaultAnsibleController'
default = default_ansible_controller(default_ansible_controller_id)
print("default control is {0}".format(default))
for host in targeted_hosts(deltas=specification.deltas):
    print(host)
    if host.ansibleController is None:
        if default is None:
            raise Exception("HOST {0} has not ansibleController property set but I can't assign the default Ansible Controller '{1}', it doesn't exist in the repository".format(host, default_ansible_controller_id))
        else:
            print("HOST {0} has not ansibleController property set, assign the default Ansible Controller {1}".format(host, default_ansible_controller_id))
            host.ansibleController = default
            repositoryService.update([host])
