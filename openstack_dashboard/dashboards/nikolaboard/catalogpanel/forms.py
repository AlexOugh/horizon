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

import json
import logging

from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_variables  # noqa

from oslo_utils import strutils
import six

from horizon import exceptions
from horizon import forms
from horizon import messages

from openstack_dashboard import api


LOG = logging.getLogger(__name__)


class LaunchCatalogForm(forms.SelfHandlingForm):

    catalog_id = forms.CharField(label=_("Catalog ID"),
                                required=False,
                                widget=forms.HiddenInput())
    name = forms.CharField(max_length=255, label=_("Stack Name"), initial='poc_stackname_')
    no_autocomplete = True


    def _set_default(self, field_name, default_value, readonly=True):
        if field_name not in self.fields:   return
        self.fields[field_name].initial = default_value
        if readonly:
            readonlyInput = forms.TextInput(attrs={'readonly': 'readonly'})
            self.fields[field_name].widget = readonlyInput


    def __init__(self, request, *args, **kwargs):
        super(LaunchCatalogForm, self).__init__(request, *args, **kwargs)

        catalog_id = kwargs['initial'].get('catalog_id', None)

        # add the fields from the input parameters of the selected catalog dynamically
        for param in kwargs['initial'].get('catalog_parameters', []):
            self.fields[param] = forms.CharField(label=_(param), required=True)
            self.fields[param].initial = 'poc_%s_' % param.lower()

        # set the default values
        self._set_default('ExternalNetworkId', 'd28232f2-344f-43ed-89c0-6379c979f30d')
        self._set_default('KeyName', 'managedos_key')
        self._set_default('ImageName', 'centos')
        self._set_default('FlavorName', 'm1.small')
        self._set_default('IPRange', '10.10.  .0/24', False)
        self._set_default('GatewayIP', '10.10.  .254', False)


    #@sensitive_variables('password')
    def handle(self, request, data):
        print data
        try:
            api.nikola.catalog.launch_catalog(self.request, data['catalog_id'], data)
            messages.success(request, _("Service catalog launch started."))
            return True
        except Exception:
            exceptions.handle(request)
