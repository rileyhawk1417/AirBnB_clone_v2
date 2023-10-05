#!/usr/bin/python3
"""Pack & Deploy the static files to the servers"""
import os
from datetime import datetime as time
from fabric.api import env,\
    put, run, task, sudo,\
    local, runs_once


env.hosts = ['100.26.221.74', '52.87.254.201']
env.user = 'ubuntu'


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


@task
def do_deploy(archive_path):
    """Deploy code to web servers"""

    if os.path.exists(archive_path) is not True:
        return False
    # year, month, day, hour, minutes, seconds
    """
    archive_date = time.strptime(\
    archive_path[20:].split('.')[0], "%Y%m%d%H%M%S")
    """
    archive_date = archive_path[20:].split('.')[0]

    # Place archive in tmp
    put("versions/web_static_{}.tgz".format(archive_date), '/tmp/')

    # mkdir in releases
    folder_name = "web_static_{}".format(archive_date)
    run("mkdir -p /data/web_static/releases/{}".format(folder_name))

    # Uncompress files to new dir
    tar_name = "/tmp/web_static_{}.tgz".format(archive_date)
    tar_dir = "/data/web_static/releases/web_static_{}".format(archive_date)
    run("tar -xzf {} -C {}".format(tar_name, tar_dir))

    # Move files from subfolder to parent
    run("mv /data/web_static/releases" +
        "/web_static_{}/web_static/*".format(archive_date) +
        " /data/web_static/releases" +
        "/web_static_{}".format(archive_date))

    # Delete empty folder
    run("rm -rf /data/web_static/releases" +
        "/web_static_{}/web_static".format(archive_date))

    # Delete current symlink
    run("rm -rf /data/web_static/current")

    # Create a new symlink
    run("ln -sf /data/web_static/releases/" +
        "web_static_{} /data/web_static/current".format(archive_date))

    # Cleanup tmp
    run("rm /tmp/web_static_{}.tgz".format(archive_date))

    sudo("service nginx restart")
    print("New version deployed!")


@task
def deploy():
    archive = do_pack()
    if archive is None:
        return False
    return do_deploy(archive_path=archive)
