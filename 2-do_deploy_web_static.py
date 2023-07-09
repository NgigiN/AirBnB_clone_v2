#!/usr/bin/python3
"""
script that distributes the archive to webservers
"""
import os.path
from fabric.api import *
from fabric.operations import put, run, sudo
env.hosts = ['100.26.240.218', '18.206.208.189']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """ To infinity... """
    if (os.path.isfile(archive_path) is False):
        return False
    try:
        put(archive_path, '/tmp/')

        # create target dir
        timestamp = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/\
releases/web_static_{}/'.format(timestamp))

        # uncompress archive and delete .tgz
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C \
/data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        # remove archive
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # move contents into host web_static
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* \
/data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

        # remove extraneous web_static dir
        run('sudo rm -rf /data/web_static/releases/\
web_static_{}/web_static'
            .format(timestamp))

        # delete pre-existing sym link
        run('sudo rm -rf /data/web_static/current')

        # re-establish symbolic link
        run('sudo ln -s /data/web_static/releases/\
web_static_{}/ /data/web_static/current'.format(timestamp))

    except:
        return False

    # return True on success
    return True
