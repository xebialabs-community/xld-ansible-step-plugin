<#--

    Copyright 2020 XEBIALABS

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

-->
{
    "devops_as_code_directory": "${ansibleController.devopsAsCodeDirectory}",
     "container" : {
        "id": "${deployed.container.id}",
        "name":"${deployed.container.name}",
        "address": "${deployed.container.address}",
        "connectionType": "${deployed.container.connectionType}",
        "os": "${deployed.container.os}",
        "port": "${deployed.container.port}",
        "username": "${deployed.container.port}",
        "privateKeyFile": "${deployed.container.privateKeyFile}",
     },
     "container_id": "${deployed.container.id}",
     "container_name": "${deployed.container.name}",
     "deployedApplication" :{
        "environment" : {
            "id": "${deployedApplication.environment.id}",
            "name": "${deployedApplication.environment.name}"
        },
        "version" : {
            "id": "${deployedApplication.version.id}",
            "name": "${deployedApplication.version.name}",
            "application":{
                "id": "${deployedApplication.version.application.id}",
                "name": "${deployedApplication.version.application.name}",
            }
        }
     },
<#list variables?keys as envVar>
    "${envVar}":"${variables[envVar]}",
</#list>
}