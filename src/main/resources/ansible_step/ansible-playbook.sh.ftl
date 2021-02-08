<#--

    Copyright 2021 XEBIALABS

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

-->
export PYTHONUNBUFFERED=1
export ANSIBLE_CONFIG=ansible.cfg

echo "${devopsAsCodeTemplate}" > ${deployed.name}.j2

<#assign verbose=""/>
<#if ansibleController.debug>
<#assign verbose="-v"/>
echo "= xldeploy_playbook.yml ="
cat -n xldeploy_playbook.yml

echo "= inventory = "
cat ansible_step/inventory/xldeploy_ansible_inventory

echo "= extra vars = "
cat ansible_step/xldeploy_extravars.json

echo "= ansible.cfg = "
cat ansible.cfg

echo "= ${deployed.name}.j2 = "
cat ${deployed.name}.j2

echo "------ "
find . -ls
echo "------ "
cp -r . /tmp/ANSIBLE/
</#if>

<#list galaxyRoles>
<#items as role>
${ansibleController.ansibleGalaxyPath} install ${role}
${role}_EXIT_CODE=$?
if [ ${role}_EXIT_CODE -eq 0 ]; then
echo ERROR: Error when installing ${role}, EXIT
exit 10
fi
</#items>
${ansibleController.ansibleGalaxyPath} list
</#list>

echo "${ansibleController.ansiblePlaybookPath} --inventory-file=ansible_step/inventory/xldeploy_ansible_inventory ${verbose} --extra-vars "@ansible_step/xldeploy_extravars.json" ./xldeploy_playbook.yml"
${ansibleController.ansiblePlaybookPath} --inventory-file=ansible_step/inventory/xldeploy_ansible_inventory ${verbose} --extra-vars "@ansible_step/xldeploy_extravars.json" ./xldeploy_playbook.yml




