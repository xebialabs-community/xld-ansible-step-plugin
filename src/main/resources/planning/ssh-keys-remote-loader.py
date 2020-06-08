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
