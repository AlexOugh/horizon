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

class MethodParam():

    def __init__(self, param_json):
        self.id = param_json['name']
        self.name = param_json['name']
        self.kind = param_json['kind']
        self.description = param_json['description']
        self.required = param_json['required']
        self.type = param_json['type']


class ServiceMethod():

    def __init__(self, method_json):
        self.id = method_json['name']
        self.name = method_json['name']
        self.kind = method_json['kind']
        self.description = method_json['description']
        self.documentation = method_json['documentation']
        self.params = []
        for param in method_json['params']:
            self.params.append(MethodParam(param))


class ServiceRegistry():
    
    def __init__(self, registry_json):
        self.id = registry_json['name']
        self.name = registry_json['name']
        self.kind = registry_json['kind']
        self.version = registry_json['version']
        self.description = registry_json['description']
        self.documentation = registry_json['documentation']
        self.category = registry_json['category']
        self.methods = []
        for method in registry_json['methods']:
            self.methods.append(ServiceMethod(method))


def list_registries(request, search_opts=None):

    from nikola_api import NikolaAPI
    nikapi = NikolaAPI()
    args = {}
    res = nikapi.send(url='/useast1/nikola/r2/RegistryService/search', data=json.dumps(args))
    print res['result']['result']
    registries = []
    for sregistry in res['result']['result']:
        registries.append(ServiceRegistry(json.loads(sregistry)['services'][0]))

    has_prev_data = False
    has_more_data = False
    return (registries, has_more_data, has_prev_data)


def get_registry(request, service_name):

    from nikola_api import NikolaAPI
    nikapi = NikolaAPI()
    args = args={'service_name':service_name}
    res = nikapi.send(url='/useast1/nikola/r2/RegistryService/search', data=json.dumps(args))
    sregistry = res['result']['result'][0]
    return ServiceRegistry(json.loads(sregistry)['services'][0])


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
    