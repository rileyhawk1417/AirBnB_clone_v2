#!/usr/bin/python3
"""Fabfile module to help pack web files"""
import os
from datetime import datetime as time
from fabric.api import local, runs_once


@runs_once
def do_pack():
    """Function does compression & size estimation"""

    if not os.path.isdir("versions"):
        os.mkdir("versions")
    current_time = time.now()
    tarball = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        current_time.year,
        current_time.month,
        current_time.day,
        current_time.hour,
        current_time.minute,
        current_time.second
    )
    try:
        print("Pack web files into tarball {}".format(tarball))
        local("tar -cvzf {} web_static".format(tarball))
        tar_size = os.stat(tarball).st_size
        print("web_static packed: {} -> {} Bytes".format(tarball, tar_size))
    except Exception:
        tarball = None
    return tarball
