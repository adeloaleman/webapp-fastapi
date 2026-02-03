# %%

import json 
from IPython import get_ipython
from typing import List


# %%

SSH = 'ssh -o StrictHostKeyChecking=no'
SCP = 'scp -o StrictHostKeyChecking=no'

class Server:
    def __init__(self,
            id_name = None,
            ip = None,
            ssh_key_path = None,
            username = 'ubuntu',
            home_path = '/home/ubuntu',
            workspace_path = '/home/ubuntu',
        ):
        self.id_name = id_name
        self.ip = ip
        self.ssh_key_path = ssh_key_path
        self.username = username
        self.home_path = home_path
        self.workspace_path = workspace_path
    
    def __str__(self):
        return json.dumps(self.__dict__, indent=4)

    def __repr__(self):
        return str(self)


def scp_file_to_servers(
        servers:List['Server'] = None,
        file_path = '../cybots',
        file_name_at_server = '',
        server_dir_path_rth = '.',
        tar_gz = False,
        exclusions = ['.venv', 'cybots/data/*', 'cybots/temp/*', '*d4t4*'],
        delete_old_file_before_recopying = False
    ):
    """
    :``file_name_at_server`` is not working well. This would be used just in case you want to rename the file at the server.
    """
    servers = servers
    file_name = file_path.split('/')[-1]
    local_dir_path = '/'.join(file_path.split('/')[0:-1])
    _file_name = file_name
    if tar_gz:
        if exclusions: exclusions=' '.join([f"--exclude='{path}'" for path in exclusions])
        get_ipython().system(f"tar -czf {local_dir_path}/{_file_name}.tar.gz {exclusions} {local_dir_path}/{_file_name}")
        _file_name = f'{_file_name}.tar.gz'
    for s in servers:
        server_dir_path = f'{s.home_path}/{server_dir_path_rth}'
        if delete_old_file_before_recopying:
            get_ipython().system(f"{SSH} {s.username}@{s.ip} '''cd {server_dir_path} ; gio trash {file_name}''' ")
        command = f"{SCP}  {local_dir_path}/{_file_name}  {s.username}@{s.ip}:{server_dir_path}/{file_name_at_server}"
        print(command)
        get_ipython().system(command)
        if tar_gz:
            get_ipython().system(f"{SSH} {s.username}@{s.ip} '''cd {server_dir_path} ; tar xzf {_file_name} ; gio trash {_file_name}''' ")


# %%

servers = [
    Server(
        id_name = 'sinfronteras',
        username = 'ubuntu',
        home_path = '/home/ubuntu',
        ssh_key_path = 'cybots',
        ip = '62.171.143.243',
    ),
]

scp_file_to_servers(
    servers,
    file_path = '../fastapi',
    tar_gz = True,
    delete_old_file_before_recopying=False
)


