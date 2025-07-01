"""
General utilities
"""
import typing
from .plugins import PluginManager


class BackupManagerPlugin(typing.Protocol):
    """
    Stand-in class for how backup manager plugins look
    """
    def performBackup(self)->bool:
        """
        Perform a backup
        """


backupManagerPlugins=PluginManager[BackupManagerPlugin](
    'backup_plan.backup_manager')
