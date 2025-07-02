#!/usr/bin/env python3
"""
Tools to handle backup manager plugins
"""
import typing
from backup_plan.plugins import PluginManager


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


def main(args:typing.Iterable[str])->int:
    """
    Run this like from the command line
    """
    _=args
    print('Registered backup manager plugins:')
    for plugin in backupManagerPlugins.keys(): # pylint: disable=duplicate-code
        print(plugin)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
