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

import logging

from django.conf import settings
#from heatclient import client as heat_client

from horizon.utils import functions as utils
#from horizon.utils.memoized import memoized  # noqa
#from openstack_dashboard.api import base
from openstack_dashboard.api.nikola.heat import *

LOG = logging.getLogger(__name__)


def stacks_list(request, marker=None, sort_dir='desc', sort_key='created_at',
                paginate=False):
    limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
    page_size = utils.get_page_size(request)

    if paginate:
        request_size = page_size + 1
    else:
        request_size = limit

    kwargs = {'sort_dir': sort_dir, 'sort_key': sort_key}
    if marker:
        kwargs['marker'] = marker

    stacks = nikola_stacks_list(request.session['auth_ref'], marker, sort_dir, sort_key, request_size)

    has_prev_data = False
    has_more_data = False

    if paginate:
        if len(stacks) > page_size:
            stacks.pop()
            has_more_data = True
            if marker is not None:
                has_prev_data = True
        elif sort_dir == 'asc' and marker is not None:
            has_more_data = True
        elif marker is not None:
            has_prev_data = True
    return (stacks, has_more_data, has_prev_data)


def stack_delete(request, stack_id):
    return nikola_stack_delete(request.session['auth_ref'], stack_id)


def stack_get(request, stack_id):
    return nikola_stack_get(request.session['auth_ref'], stack_id)


def template_get(request, stack_id):
    return nikola_template_get(request.session['auth_ref'], stack_id)


def stack_create(request, password=None, **kwargs):
    return nikola_stack_create(request.session['auth_ref'], **kwargs)


def stack_update(request, stack_id, password=None, **kwargs):
    return nikola_stack_update(request.session['auth_ref'], stack_id, **kwargs)


def events_list(request, stack_name):
    return nikola_events_list(request.session['auth_ref'], stack_name)


def resources_list(request, stack_name):
    return nikola_resources_list(request.session['auth_ref'], stack_name)


def resource_get(request, stack_id, resource_name):
    return nikola_resource_get(request.session['auth_ref'], stack_id, resource_name)


def resource_metadata_get(request, stack_id, resource_name):
    return nikola_resource_metadata_get(request.session['auth_ref'], stack_id, resource_name)


def template_validate(request, **kwargs):
    return nikola_template_validate(request.session['auth_ref'], **kwargs)


def action_check(request, stack_id):
    return nikola_action_check(request.session['auth_ref'], stack_id)


def resource_types_list(request):
    return nikola_resource_types_list(request.session['auth_ref'])


def resource_type_get(request, resource_type):
    return nikola_resource_type_get(request.session['auth_ref'], resource_type)
