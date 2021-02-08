<#--

    Copyright 2021 XEBIALABS

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

-->
---
- hosts: all
<#if become>  
  become: true
</#if>
<#if variableFile?has_content>  
  vars_files:
    - ${deployed.file.path}/${variableFile}
</#if>
  roles:
<#list roles as role>
    - { role: ${role} }
</#list>
  tasks:
<#list deployed.devopsAsCodeTemplates as template>
    - name: Generate the Devops-As-Code
      template:
        src: ${deployed.name}.j2
        dest: /tmp/digital.ai_xldeploy.yaml
        mode: 0755
    - name: Fetch the Devops-As-Code yaml file on the master
      fetch:
        src: /tmp/digital.ai_xldeploy.yaml
        dest: "{{ devops_as_code_directory }}"
        flat: no
</#list>

