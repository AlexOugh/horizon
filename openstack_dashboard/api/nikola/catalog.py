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

from heat import *

#LOG = logging.getLogger(__name__)

class ServiceCatalog():
    
    def __init__(self, catalog_json):
        self.id = catalog_json['id']
        self.name = catalog_json['name']
        self.description = catalog_json['description']
        self.availability = catalog_json['availability']
        self.content = catalog_json['content']


def list_catalogs(request, search_opts=None):

    from nikola_api import NikolaAPI
    nikapi = NikolaAPI()
    res = nikapi.send(url='/useast1/nikola/r2/openstack/list_catalogs', data='{"all":null}')
    print 'result = %s' % res['result']
    catalogs = []
    for catalog in res['result']['result']:
        catalogs.append(ServiceCatalog(catalog))

    has_prev_data = False
    has_more_data = False
    return (catalogs, has_more_data, has_prev_data)
