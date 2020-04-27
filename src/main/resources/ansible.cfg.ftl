[defaults]
# Host key checking is disabled by default (ANSIBLE_HOST_KEY_CHECKING=false)
host_key_checking = False
#no color else the output in XLD will be ugly :-/ export ANSIBLE_FORCE_COLOR=false
nocolor = 1
# Paths to search for roles, colon separated
roles_path = ${ansibleController.ansibleRolePath}:${deployed.file.path}/roles
