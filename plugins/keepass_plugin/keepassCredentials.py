"""
Plugin to read credentials from keepass
"""
import typing
import subprocess
from pathlib import Path
try:
    from pykeepass import PyKeePass
    hasPyKeePass=True
except ImportError:
    hasPyKeePass=False


class Plugin:
    """
    Credential manager plugin
    """
    def __init__(self,
        db_path:Path,
        password:typing.Optional[str]=None,
        keyfile:typing.Optional[Path]=None):
        """ """
        self.db_path=db_path
        self.password=password
        self.keyfile=keyfile
        self.loadDatabase()

    def loadDatabase(self)->None:
        """
        Open a KeePass database.
        """
        if not hasPyKeePass:
            return
        if self.keyfile is not None:
            self.keyfile=str(self.keyfile)
        self.kp=PyKeePass(str(self.db_path),
            password=self.password,keyfile=self.keyfile)

    def getCredentials(self,
        username:str
        )->typing.Tuple[str,str]:
        """
        Locate entry by title and return (username,password).
        Raises ValueError if entry not found.
        """
        if not hasPyKeePass:
            # revert to command line as a fallback
            res = subprocess.run(
                ["keepassxc-cli","show","--field","Password",username],
                capture_output=True,text=True,check=True
            )
            return res.stdout.strip()
        entry=None
        for entry in self.kp.find_entries(title=username,first=True):
            break
        if not entry:
            raise ValueError(f"Entry '{username}' not found")
        return entry.username or "",entry.password or ""
