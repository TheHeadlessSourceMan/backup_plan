"""
Tools to determine whether a directory has changed
"""
import typing
import datetime
import hashlib
from pathlib import Path


def computeHash(path:Path)->str:
    """
    Compute a hash of an entire directory
    """
    h = hashlib.sha256()
    for p in sorted(path.rglob('*')):
        if p.is_file():
            h.update(str(p.relative_to(path)).encode())
            h.update(p.read_bytes())
    return h.hexdigest()

def computeTotalSize(path:Path)->int:
    """
    Compute total size of a file or entire directory
    """
    return sum([p.stat().st_size for p in path.rglob('*')])

def computeLastModifiedTime(path:Path)->datetime.datetime:
    """
    Compute the last modified time of an entire directory
    """
    newestTimestamp=max([p.stat().st_mtime for p in path.rglob('*')])
    return datetime.datetime.fromtimestamp(newestTimestamp)

def hasChanged(
    path:Path,
    lastHash:typing.Optional[str]=None,
    sinceTimestamp:typing.Optional[datetime.datetime]=None,
    lastSize:typing.Optional[int]=None
    )->bool:
    """
    Check to see if a file or directory has changed
    """
    if lastSize is not None \
        and computeTotalSize(path)!=lastSize:
        return True
    if sinceTimestamp is not None \
        and computeLastModifiedTime(path)!=sinceTimestamp:
        return True
    if lastHash is not None \
        and computeHash(path)!=lastHash:
        return True
    return False
