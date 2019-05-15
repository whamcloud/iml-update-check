#!/usr/bin/python

# Copyright (c) 2019 DDN. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import os
import json
from urlparse import urljoin
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from yum import YumBase

# Disable insecure requests warning
# So we don't break our syslog handler.
# This (disabled) warning is expected due to our use of
# self-signed certificates when we communicate between
# the agent and manager.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

yb = YumBase()
yb.preconf.debuglevel = 0
yb.preconf.errorlevel = 0
yb.getReposFromConfigFile("/etc/yum.repos.d/Intel-Lustre-Agent.repo")
repos = map(lambda x: x.id, yb._repos.listEnabled())

yb.cleanMetadata()

has_updates = False

for repo in repos:
    ypl = yb.doPackageLists(pkgnarrow="updates", repoid=repo)
    has_updates |= len(ypl.updates) > 0

yb.close()

resp = requests.post(
    urljoin(os.environ["IML_MANAGER_URL"], "iml_has_package_updates"),
    cert=(os.environ["IML_CERT_PATH"], os.environ["IML_PRIVATE_KEY_PATH"]),
    verify=False,
    headers={"Content-Type": "application/json"},
    data=json.dumps(has_updates),
)

print("Found updates: {}".format(has_updates))
print("Manager responded, status code: {0}".format(resp.status_code))
