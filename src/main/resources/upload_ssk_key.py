from overtherepy import OverthereHostSession
from java.io import File
import sys

session = OverthereHostSession(container.ansibleController.host)

source = session.local_file(File(container.privateKeyFile))
target = session.remote_file(target_path)
if target.exists():
    print("File exists, delete it !")
    target.delete()

print('Copy {0} -> {1}'.format(source, target))
session.copy_to(source, target)
chmod = "chmod 400 {0}".format(target_path)
print(chmod)
response = session.execute(chmod)
