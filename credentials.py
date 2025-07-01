"""
All credential managers
"""
import typing
from .plugins import PluginManager


class CredentialsPlugin(typing.Protocol):
    """
    Stand-in class for how credential manager plugins look
    """
    def getCredentials(self,username:str)->"Credentials":
        """
        Get credentials
        """


class Credentials:
    """
    A set of credentials
    """
    def __init__(self,username:str,password:str):
        self.username=username
        self.password=password


class CredentialManagers(PluginManager[CredentialsPlugin]):
    """
    All credential managers
    """

    def __init__(self,params:typing.Dict[str,typing.Any]):
        self.params=params
        PluginManager.__init__(self,'backup_plan.credential_manager')

    def getCredentials(self,
        manager:str='keepass',
        username:str=''
        )->Credentials:
        """
        Get credentials from a specific credentials manager
        """
        return self[manager].getCredentials(username)
