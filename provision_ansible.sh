apt update
apt install --yes software-properties-common
apt-add-repository --yes --update ppa:ansible/ansible
apt install --yes ansible
ansible-playbook --version
echo "-- DONE --"
