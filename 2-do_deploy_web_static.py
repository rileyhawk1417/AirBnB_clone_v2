#!/usr/bin/python3
"""Fabfile module to help pack web files"""
import os
from datetime import datetime as time
from fabric.api import env, put, run, runs_once

env.hosts = ['100.26.221.74', '52.87.254.201']
env.user = 'ubuntu'

@runs_once
def do_deploy():
    """Deploy code to web servers"""
 
    # year, month, day, hour, minutes, seconds
    date_now = time.now().strftime("%Y%m%d%H%M%S")

    # Place archive in tmp
    put("versions/web_static_{}.tgz".format(date_now), '/tmp/')

    # mkdir in releases
    run("mkdir -p /data/web_static/releases/web_static_{}".format(date_now))

    # Uncompress files to new dir 
    run ("tar -xzf /tmp/web_static_{}.tgz -C\
    /data/web_static/releases/web_static_{}".format(date_now, date_now))

    # Move files from subfolder to parent
    run("mv /data/web_static/releases/web_static_{}/web_static/*\
    /data/web_static/releases/web_static_{}".format(date_now, date_now))

    # Delete empty folder
    run("rm -rf /data/web_static/releases/web_static_{}/web_static_")

    # Delete current symlink
    run("rm -f /data/web_static/current")

    # Create a new symlink
    run("sudo ln -sf /data/web_static/releases/web_static_{}\
    /data/web_static/current/".format(date_now))
