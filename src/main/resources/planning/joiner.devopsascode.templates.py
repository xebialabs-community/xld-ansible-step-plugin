#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


from org.apache.commons.io import IOUtils


def to_string(from_file, charset):
    return IOUtils.toString(from_file.getInputStream(), charset)


def roles():
    result = []
    for _delta in specification.deltas:
        deployed = _delta.deployedOrPrevious
        if (_delta.operation == "CREATE" or _delta.operation == "MODIFY") and deployed.type == "ansible.Roles":
            result.append(deployed)
    return set(result)


for role in roles():
    data = ""
    for template in role.devopsAsCodeTemplates:
        content = to_string(template.file, "UTF-8")
        data = data + content
    #print(data)
    role.computedDevopsAsCodeTemplate = data
