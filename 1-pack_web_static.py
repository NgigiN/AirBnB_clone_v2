#!/usr/bin/python3
# Fabfile to generate a .tgz archive from the contents of web_static

import os.path
from datetime import date
from time import strftime
from fabric.api import local


def do_pack():
    """A script that generates archive the contents of web_static folder"""

    file_name = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(file_name))

        return "versions/web_static_{}.tgz".format(file_name)

    except Exception as e:
        return None
