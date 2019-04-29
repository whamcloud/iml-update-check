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

yp = YumBase()
yp.preconf.debuglevel = 0
yp.preconf.errorlevel = 0
yp.getReposFromConfig()
yp.doSackFilelistPopulate()

packages = ["python2-iml-agent"]

if "IML_PROFILE_PACKAGES" in os.environ:
    packages += os.environ["IML_PROFILE_PACKAGES"].split(",")

ypl = yp.doPackageLists(pkgnarrow="updates", patterns=packages)

has_updates = len(ypl.updates) > 0

if "IML_PROFILE_REPOS" in os.environ:
    for bundle in os.environ["IML_PROFILE_REPOS"].split(","):
        if bundle == "external":
            continue
        ypl = yp.doPackageLists(pkgnarrow=["updates"], repoid=bundle)
        has_updates |= len(ypl.updates) > 0

yp.close()

resp = requests.post(
    urljoin(os.environ["IML_MANAGER_URL"], "iml_has_package_updates"),
    cert=(os.environ["IML_CERT_PATH"], os.environ["IML_PRIVATE_KEY_PATH"]),
    verify=False,
    headers={"Content-Type": "application/json"},
    data=json.dumps(has_updates),
)

print("Manager responded, status code: {0}".format(resp.status_code))
