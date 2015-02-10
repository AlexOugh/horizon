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

class IAMUser():
    
    def __init__(self, iam_json):
        self.id = iam_json['id']
        self.name = iam_json['name']
        '''self.description = catalog_json['description']
        self.availability = catalog_json['availability']
        self.content = catalog_json['content']
        self.parameters = []
        for key in catalog_json['input_params'].keys():
            self.parameters.append(key)'''


def list_iam_users(request, search_opts=None):

    '''from nikola_api import NikolaAPI
    nikapi = NikolaAPI()
    res = nikapi.send(url='/useast1/nikola/r2/openstack/list_catalogs', data='{"all":null}')
    catalogs = []
    for catalog in res['result']['result']:
        catalogs.append(ServiceCatalog(catalog))'''
    
    iam_users = []
    iam_users.append(IAMUser({'id':'id1', 'name':'name1'}))
    iam_users.append(IAMUser({'id':'id2', 'name':'name2'}))

    has_prev_data = False
    has_more_data = False
    return (iam_users, has_more_data, has_prev_data)


def get_iam_user(request, iam_user_id):

    '''from nikola_api import NikolaAPI
    nikapi = NikolaAPI()
    res = nikapi.send(url='/useast1/nikola/r2/openstack/get_registry', data='{"id":"%s"}' % (registry_id))
    return ServiceRegistry(res['result']['result'])'''
    return IAMUser({'id':iam_user_id, 'name':'name of %s' % iam_user_id})


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
    