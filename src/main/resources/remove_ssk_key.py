from overtherepy import OverthereHostSession

session = OverthereHostSession(container.ansibleController.host)
target = session.remote_file(target_path)

print('Delete {0}'.format(target))
target.delete()
