"""
Plugin to backup using sftp
"""
import typing
import os
import subprocess
import paramiko


class Plugin:
    """
    Plugin to backup using sftp
    """
    def __init__(self,config:typing.Dict[str,typing.Any]):
        self.host=config["location"]
        self.username=config["username"]
        self.remote_path=config["name"]
        self.pass_entry=f"{self.username}@{self.host}"

    def _get_password(self):
        res=subprocess.run(
            ["keepassxc-cli","show","--field","Password",self.pass_entry],
            capture_output=True,text=True,check=True
        )
        return res.stdout.strip()

    def run(self,local_path):
        """
        run the backup
        """
        pw=self._get_password()
        transport=paramiko.Transport((self.host,22))
        transport.connect(username=self.username,password=pw)
        sftp=paramiko.SFTPClient.from_transport(transport)
        self._upload_dir(sftp,local_path,self.remote_path)
        sftp.close()
        transport.close()

    def _upload_dir(self,sftp,local,remote):
        try:
            sftp.stat(remote)
        except FileNotFoundError:
            sftp.mkdir(remote)
        for entry in os.listdir(local):
            lp=os.path.join(local,entry)
            rp=os.path.join(remote,entry)
            if os.path.isdir(lp):
                self._upload_dir(sftp,lp,rp)
            else:
                sftp.put(lp,rp)
