#!/usr/bin/python
# Copyright (c) 2018 DDN. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import os
import sys
import json
from dnf import Base, exceptions

# Disable insecure requests warning
# So we don't break our syslog handler.
# This (disabled) warning is expected due to our use of
# self-signed certificates when we communicate between
# the agent and manager.
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests

base = Base()
base.read_all_repos()
base.fill_sack()

repos = filter(lambda x: x.repofile == os.environ['IML_REPO_PATH'],
               base.repos.all())
ids = map(lambda x: x.id, repos)

upgrades = base.sack.query().filter(reponame=ids).upgrades().latest().run()

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
    '{0}iml_has_package_updates'.format(os.environ['IML_MANAGER_URL']),
    cert=(os.environ['IML_CERT_PATH'], os.environ['IML_PRIVATE_KEY_PATH']),
    verify=False,
    headers={'Content-Type': 'application/json'},
    data=json.dumps(has_updates))

print("Manager responded, status code: {0}".format(resp.status_code))
