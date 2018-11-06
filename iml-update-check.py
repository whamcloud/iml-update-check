#!/usr/bin/python

# Copyright (c) 2018 DDN. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import os
import sys
import json
from dnf import Base, exceptions
from urlparse import urljoin

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable insecure requests warning
# So we don't break our syslog handler.
# This (disabled) warning is expected due to our use of
# self-signed certificates when we communicate between
# the agent and manager.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

base = Base()
base.read_all_repos()
base.fill_sack()


def filter_unused(base, ids, name):
    """Given a package name, determines if it or any of it's parents
    are installed, and that they come from an expected repo.
    """
    names = [x.name for x in base.sack.query().filter(
        reponame=ids).filter(requires=name).run()] + [name]

    installed_parents = [x.from_repo.replace('@', '', 1) for x in base.sack.query().filter(
        name=names).installed().run()]

    return any(x in ids for x in installed_parents)


repos = filter(lambda x: x.repofile == os.environ['IML_REPO_PATH'],
               base.repos.all())

ids = map(lambda x: x.id, repos)

upgrades = base.sack.query().filter(reponame=ids).upgrades().latest().run()
upgrades = filter(lambda x: filter_unused(base, ids, x.name), upgrades)

map(base.package_upgrade, upgrades)

has_updates = False

try:
    has_updates = bool(base.resolve())
except exceptions.DepsolveError as e:
    print("Error resolving deps %{0}".format(e))
finally:
    base.close()

print("Sending result, has updates: {0}".format(has_updates))

resp = requests.post(
    urljoin(os.environ['IML_MANAGER_URL'], 'iml_has_package_updates'),
    cert=(os.environ['IML_CERT_PATH'], os.environ['IML_PRIVATE_KEY_PATH']),
    verify=False,
    headers={'Content-Type': 'application/json'},
    data=json.dumps(has_updates))

print("Manager responded, status code: {0}".format(resp.status_code))
