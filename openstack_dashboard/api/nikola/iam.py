# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

#import logging

#from django.conf import settings
#from heatclient import client as heat_client

#from horizon.utils import functions as utils
#from horizon.utils.memoized import memoized  # noqa
#from openstack_dashboard.api import base

import json
from heat import *

#LOG = logging.getLogger(__name__)

class SSOUser():
    
    def _set_attr(self, attr_name, json_obj, json_attr):
        if json_attr in json_obj:
            setattr(self, attr_name, json_obj[json_attr])


    def __init__(self, sso_info):
        self._set_attr('guid', sso_info, 'guid')
        self._set_attr('first_name', sso_info, 'first_name')
        self._set_attr('last_name', sso_info, 'last_name')
        self._set_attr('locked', sso_info, 'locked')
        self._set_attr('phone', sso_info, 'phone')
        self._set_attr('locale', sso_info, 'locale')
        self._set_attr('company_name', sso_info, 'company_name')
        self._set_attr('company_guid', sso_info, 'company_guid')
        self._set_attr('disabled', sso_info, 'disabled')
        self._set_attr('timezone', sso_info, 'timezone')
        self._set_attr('nickname', sso_info, 'nickname')
        self._set_attr('email', sso_info, 'email')


class OpenStackUser():
    
    def _set_attr(self, attr_name, json_obj, json_attr):
        if json_attr in json_obj:
            setattr(self, attr_name, json_obj[json_attr])


    def __init__(self, openstack_info):
        self._set_attr('id', openstack_info, 'id')
        self._set_attr('name', openstack_info, 'name')
        self._set_attr('domain_id', openstack_info, 'domain_id')
        self._set_attr('enabled', openstack_info, 'enabled')
        self._set_attr('email', openstack_info, 'email')
        self._set_attr('op_tenant_name', openstack_info, 'op_tenant_name')


class IAMUser():
    
    def _set_attr(self, attr_name, json_obj, json_attr):
        if json_attr in json_obj:
            setattr(self, attr_name, json_obj[json_attr])


    def __init__(self, iam_user):
        iam_json = iam_user['iam']
        self._set_attr('id', iam_json, 'id')
        self._set_attr('op_username', iam_json, 'op_username')
        self._set_attr('sso_uuid', iam_json, 'sso_uuid')
        self._set_attr('op_user_id', iam_json, 'op_user_id')
        self._set_attr('op_tenant_name', iam_json, 'op_tenant_name')
        self._set_attr('op_keystone_server', iam_json, 'op_keystone_server')
        self._set_attr('op_auth_urls', iam_json, 'op_auth_urls')
        self._set_attr('op_keystone_region', iam_json, 'op_keystone_region')
        if 'sso' in iam_user:
            self.sso = SSOUser(iam_user['sso'])
        if 'openstack' in iam_user:
            self.openstack = OpenStackUser(iam_user['openstack'])


def list_iam_users(request, search_opts=None):

    auth_ref = request.session['auth_ref']
    catalog = auth_ref.get('catalog')
    endpoint = next(ep['url'] for ep in next(s['endpoints'] for s in catalog if s['name'] == 'keystone') if ep['interface']=='admin')
    token = auth_ref['auth_token']  

    from nikola_api import NikolaAPI
    nikapi = NikolaAPI()
    data = {'all':''}
    res = nikapi.send(url='/useast1/nikola/r2/iam/list_users', data=json.dumps(data))
    print res
    iam_users = []
    for iam_user in res['result']['result']:
        iam_users.append(IAMUser(iam_user))
    
    has_prev_data = False
    has_more_data = False
    return (iam_users, has_more_data, has_prev_data)


def get_iam_user(request, iam_user_id):

    auth_ref = request.session['auth_ref']
    catalog = auth_ref.get('catalog')
    endpoint = next(ep['url'] for ep in next(s['endpoints'] for s in catalog if s['name'] == 'keystone') if ep['interface']=='admin')
    token = auth_ref['auth_token']  

    from nikola_api import NikolaAPI
    nikapi = NikolaAPI()
    data = {'user_id':iam_user_id, 'auth_admin_url':endpoint, 'admin_token':token}
    res = nikapi.send(url='/useast1/nikola/r2/iam/get_user', data=json.dumps(data))
    print res
    return IAMUser(res['result']['result'])


"""def launch_catalog(request, catalog_id, params):
    
    auth_ref = request.session['auth_ref']
    catalog = auth_ref.get('catalog')
    endpoint = next(ep['url'] for ep in next(s['endpoints'] for s in catalog if s['name'] == 'heat') if ep['interface']=='public')
    token = auth_ref['auth_token']  
    
    from nikola_api import NikolaAPI
    nikapi = NikolaAPI()
    data = json.dumps({"id":catalog_id, "params":params, "heat_url":endpoint, "token":token})
    print data
    res = nikapi.send(url='/useast1/nikola/r2/openstack/launch_catalog', data=data)
    print res
    return res['result']['result']"""
    