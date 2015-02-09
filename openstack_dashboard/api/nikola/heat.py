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
from heatclient import client as heat_client

#from horizon.utils import functions as utils
#from horizon.utils.memoized import memoized  # noqa
#from openstack_dashboard.api import base

#LOG = logging.getLogger(__name__)


def format_parameters(params):
    parameters = {}
    for count, p in enumerate(params, 1):
        parameters['Parameters.member.%d.ParameterKey' % count] = p
        parameters['Parameters.member.%d.ParameterValue' % count] = params[p]
    return parameters


#@memoized
def heatclient(auth_ref):
    catalog = auth_ref.get('catalog')
    endpoint = next(ep['url'] for ep in next(s['endpoints'] for s in catalog if s['name'] == 'heat') if ep['interface']=='public')
    api_version = "1"
    token = auth_ref['auth_token']  
    client = heat_client.Client(api_version, endpoint=endpoint, token=token)
    client.format_parameters = format_parameters
    
    return client


def nikola_stacks_list(auth_ref, marker=None, sort_dir='desc', sort_key='created_at', request_size=1):

    kwargs = {'sort_dir': sort_dir, 'sort_key': sort_key}
    if marker:
        kwargs['marker'] = marker

    stacks_iter = heatclient(auth_ref).stacks.list(limit=request_size, **kwargs)
    stacks = list(stacks_iter)

    return stacks


def nikola_stack_delete(auth_ref, stack_id):
    return heatclient(auth_ref).stacks.delete(stack_id)


def nikola_stack_get(auth_ref, stack_id):
    return heatclient(auth_ref).stacks.get(stack_id)


def nikola_template_get(auth_ref, stack_id):
    return heatclient(auth_ref).stacks.template(stack_id)


def nikola_stack_create(auth_ref, **kwargs):
    return heatclient(auth_ref).stacks.create(**kwargs)


def nikola_stack_update(auth_ref, stack_id, **kwargs):
    return heatclient(auth_ref).stacks.update(stack_id, **kwargs)


def nikola_events_list(auth_ref, stack_name):
    return heatclient(auth_ref).events.list(stack_name)


def nikola_resources_list(auth_ref, stack_name):
    return heatclient(auth_ref).resources.list(stack_name)


def nikola_resource_get(auth_ref, stack_id, resource_name):
    return heatclient(auth_ref).resources.get(stack_id, resource_name)


def nikola_resource_metadata_get(auth_ref, stack_id, resource_name):
    return heatclient(auth_ref).resources.metadata(stack_id, resource_name)


def nikola_template_validate(auth_ref, **kwargs):
    return heatclient(auth_ref).stacks.validate(**kwargs)


def nikola_action_check(auth_ref, stack_id):
    return heatclient(auth_ref).actions.check(stack_id)


def nikola_resource_types_list(auth_ref):
    return heatclient(auth_ref).resource_types.list()


def nikola_resource_type_get(auth_ref, resource_type):
    return heatclient(auth_ref).resource_types.get(resource_type)
