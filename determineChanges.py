"""
Tools to determine whether a directory has changed
"""
import typing
import datetime
import hashlib
from pathlib import Path


def compute_hash(path:Path)->str:
    """
    Compute a hash of an entire directory
    """
    h = hashlib.sha256()
    for p in sorted(path.rglob('*')):
        if p.is_file():
            h.update(str(p.relative_to(path)).encode())
            h.update(p.read_bytes())
    return h.hexdigest()

def compute_size(path:Path)->str:
    """
    Compute total size of a file or entire directory
    """
    return sum(path.rglob('*'))

def compute_modified_time(path:Path)->datetime.datetime:
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
        and compute_size(path)!=lastSize:
        return True
    if sinceTimestamp is not None \
        and compute_modified_time(path)!=sinceTimestamp:
        return True
    if lastHash is not None \
        and compute_hash(path)!=lastHash:
        return True
    return False
