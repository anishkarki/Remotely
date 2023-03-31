from remotely.remotelyconfigmanager.config_handler import Session, Host, User

session = Session()

# Query all hosts
hosts = session.query(Host).all()
for host in hosts:
    print(f"Host: {host.hostname}, Switch Root: {host.switch_root}")
    for user in host.users:
        print(f"  User: {user.username}, Command: {user.command}")
