"""
Plugin to read credentials from keepass
"""
import typing
import subprocess
from pathlib import Path
try:
    from pykeepass import PyKeePass # type: ignore
    hasPyKeePass=True
except ImportError:
    hasPyKeePass=False


class Plugin:
    """
    Credential manager plugin
    """
    def __init__(self,
        dbPath:Path,
        password:typing.Optional[str]=None,
        keyFile:typing.Optional[Path]=None):
        """ """
        self.dbPath:Path=dbPath
        self.password:typing.Optional[str]=password
        self.keyFile:typing.Optional[Path]=keyFile
        self.loadDatabase()

    def loadDatabase(self)->None:
        """
        Open a KeePass database.
        """
        if not hasPyKeePass:
            return
        keyFile:typing.Union[None,str,Path]=self.keyFile
        if keyFile is not None:
            keyFile=str(keyFile)
        self.kp=PyKeePass(str(self.dbPath),
            password=self.password,keyfile=keyFile)

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
            return username,res.stdout.strip()
        entry=None
        for entry in self.kp.find_entries(title=username,first=True):
            break
        if not entry:
            raise ValueError(f"Entry '{username}' not found")
        return entry.username or "",entry.password or ""
