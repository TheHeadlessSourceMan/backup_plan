#!/usr/bin/env python3
"""
A backup plan.
More or less wraps a .backup_plan file in a directory.

Usually you would want to:
    BackupPlan("my_directory").runBackup()
Or possibly:
    for plan in getBackupPlans("my_directory"):
        plan.runBackup()
"""
import typing
from pathlib import Path
import json
from .determineChanges import hasChanged
from .backupManager import backupManagerPlugins


class Backup:
    """
    A single backup as specified in a backup plan
    """
    def __init__(self,
        partOfPlan:"BackupPlan",
        json:typing.Dict[str,typing.Any]):
        """ """
        self.partOfPlan=partOfPlan
        self.json=json
        self.lastHash=json.get('lastHash','')
        self.plugin=json['plugin']

    @property
    def directory(self)->Path:
        """
        Directory we are backing up
        """
        return self.partOfPlan.directory

    def runBackup(self,force:bool=False):
        """
        Run the backup
        """
        if force or hasChanged(self.directory,self.lastHash):
            backupManagerPlugins.get(self.plugin)
    run=runBackup
    __call__=runBackup


class BackupPlan:
    """
    A backup plan.
    More or less wraps a .backup_plan file in a directory.

    Usually you would want to:
        BackupPlan("my_directory").runBackup()
    Or possibly:
        for plan in getBackupPlans("my_directory"):
            plan.runBackup()
    """
    def __init__(self,directoryOrPlan:typing.Union[str,Path]):
        """
        Load backup plan
        """
        if not isinstance(directoryOrPlan,Path):
            directoryOrPlan=Path(directoryOrPlan)
        if directoryOrPlan.is_dir():
            directoryOrPlan=directoryOrPlan/".backup_plan"
        self._planFilename=directoryOrPlan
        self._json=typing.Optional[typing.List[typing.Dict]]=None

    @property
    def backups(self)->typing.Generator[Backup,None,None]:
        """
        All backups in this plan
        """
        for json in self.json:
            yield Backup(self,json)

    @property
    def directory(self)->Path:
        """
        Target directory of the backup plan
        """
        return self._planFilename.parent

    @property
    def planFilename(self)->Path:
        """
        Filename of the backup plan
        """
        return self._planFilename

    @property
    def json(self)->typing.List[typing.Dict]:
        """
        Json-compatible object representing the plan
        """
        if self._json is None:
            self.load()
        return self._json

    def load(self):
        """
        Load the plan
        """
        if self._planFilename is None:
            self._json=[]
        else:
            data=self._planFilename.read_text('utf-8',errors='ignore')
            self._json=json.loads(data)

    def save(self)->None:
        """
        Save the plan
        """
        data=json.dumps(self._json,indent=2)
        self._planFilename.write_text(data,'utf-8',errors='ignore')
        self._planFilename.close()

    def runBackups(self,force:bool=False):
        """
        Run all backups
        """
        for backup in self.backups:
            backup.runBackup(force)
    runBackup=runBackups
    run=runBackups
    __call__=runBackups


def getBackupPlan(
    directory:typing.Union[str,Path]
    )->typing.Optional[BackupPlan]:
    """
    Return BackupPlan object for directory with a .backup_plan file
    Otherwise return None.

    NOTE:if you want a BackupPlan even if the directory doesn't have
    a file yet,simply create a BackupPlan object.
    """
    plan=directory/".backup_plan"
    if plan.is_file():
        return BackupPlan(plan)
    return None


def getBackupPlans(
    directories:typing.Union[
        str,Path,typing.Iterable[typing.Union[str,Path]]]
    )->typing.Generator[BackupPlan,None,None]:
    """
    Perform a recursive search and yield a BackupPlan
    object for every directory with a .backup_plan file
    """
    if isinstance(directories,str):
        directories=[Path(directories)]
    elif isinstance(directories,Path):
        directories=[directories]
    else:
        directories=[Path(d) for d in directories]
    for directory in directories:
        bp=getBackupPlan(directory)
        if bp is not None:
            yield bp
        directories.extend(directory.iterdir())


def runAllBackups(
    directories:typing.Union[
        str,Path,typing.Iterable[typing.Union[str,Path]]],
    force:bool=False
    )->typing.Generator[BackupPlan,None,None]:
    """
    Run all backups for every directory or subdirectory with
    a backup plan.
    """
    for plan in getBackupPlans(directories):
        plan.runBackups(force)
runBackups=runAllBackups


def main(args:typing.Iterable[str])->int:
    """
    Run this like from the command line
    """
    _=args
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
