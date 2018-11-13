#!/usr/bin/python

# Copyright (c) 2018 DDN. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import os
import sys
import json
from yum import YumBase
from urlparse import urljoin

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from chroma_agent import config

# Disable insecure requests warning
# So we don't break our syslog handler.
# This (disabled) warning is expected due to our use of
# self-signed certificates when we communicate between
# the agent and manager.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

yp = YumBase()
yp.getReposFromConfig()
yp.doSackFilelistPopulate()

profile = config.get('settings', 'profile')

packages = ['python2-iml-agent']

if 'packages' in profile:
    packages += profile['packages']

ypl = yp.doPackageLists(pkgnarrow=['updates'], patterns=packages, ignore_case=True)

has_updates = len(ypl.updates) > 0

if 'bundles' in profile:
    for bundle in profile['bundles']:
        if bundle == 'external':
            continue
        ypl = yp.doPackageLists(pkgnarrow=['updates'], repoid=bundle)
        has_updates |= len(ypl.updates) > 0

yp.close()

resp = requests.post(
    urljoin(os.environ['IML_MANAGER_URL'], 'iml_has_package_updates'),
    cert=(os.environ['IML_CERT_PATH'], os.environ['IML_PRIVATE_KEY_PATH']),
    verify=False,
    headers={'Content-Type': 'application/json'},
    data=json.dumps(has_updates))

print("Manager responded, status code: {0}".format(resp.status_code))
