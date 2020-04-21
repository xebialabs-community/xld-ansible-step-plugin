#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import com.xebialabs.deployit.plugin.api.reflect.Type as Type


def query_all_containers(ci_id, results):
    # print("query {0}".format(ci_id))
    result = repositoryService.query(Type.valueOf('udm.Container'), ci_id, None, '', None, None, 0, -1)
    sub_result = []
    for sub_ci in result:
        results.append(sub_ci)
        query_all_containers(sub_ci.id, sub_result)
    results.extend(sub_result)


print("environment {0}".format(environment))
print("provisioned_host {0}".format(provisioned_host))

list_of_ci = []
query_all_containers(provisioned_host.id, list_of_ci)
members = environment.members
boundConfigurationItems = deployed.boundConfigurationItems
for ci in list_of_ci:
    print("Found {0}".format(ci))
    read_ci = repositoryService.read(ci.id)
    members.add(read_ci)
    boundConfigurationItems.add(read_ci)

environment.members = members
deployed.boundConfigurationItems = boundConfigurationItems

print environment.members

repositoryService.update([environment])

