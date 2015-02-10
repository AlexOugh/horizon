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


class LaunchWorkflowForm(forms.SelfHandlingForm):

    workflow_id = forms.CharField(label=_("Workflow ID"),
                                required=False,
                                widget=forms.HiddenInput())
    workflow_name = forms.CharField(label=_("Workflow Name"),
                                required=False,
                                widget=forms.HiddenInput())
    #name = forms.CharField(max_length=255, label=_("Stack Name"), initial='poc_stackname_')
    no_autocomplete = True


    def _set_default(self, field_name, default_value, readonly=True):
        if field_name not in self.fields:   return
        self.fields[field_name].initial = default_value
        if readonly:
            readonlyInput = forms.TextInput(attrs={'readonly': 'readonly'})
            self.fields[field_name].widget = readonlyInput


    def __init__(self, request, *args, **kwargs):
        super(LaunchWorkflowForm, self).__init__(request, *args, **kwargs)

        workflow_id = kwargs['initial'].get('workflow_id', None)
        workflow_name = kwargs['initial'].get('workflow_name', None)

        # add the fields from the input parameters of the selected catalog dynamically
        for param in kwargs['initial'].get('workflow_parameters', []):
            self.fields[param.strip()] = forms.CharField(label=_(param.strip()), required=True)

        # set the default values
        self._set_default('requester_sso_token', "3018138b45d23850ebe49c0c97faa5a60f06a0e8407b7557bc72fca9764ff523")
        self._set_default("root_op_user_name", "admin")
        self._set_default("root_op_password", "password")
        self._set_default("root_op_domain_name", "default")
        self._set_default("company_uuid", "76c6f530-40c1-446d-a5d5-a66e78605149")
        self._set_default("auth_url", "http://172.20.1.50:5000/v3/")
        self._set_default("enabled", "True")
        self._set_default("password", "Sungard05")
        self._set_default("domain_description", "Domain created for poc")
        self._set_default("project_description", "Project created for poc")
        self._set_default("email", "poc_user_  @a.com", False)
        self._set_default("first_name", "poc_first_", False)
        self._set_default("last_name", "poc_last_", False)
        self._set_default("domain_name", "poc_domain_", False)
        self._set_default("project_name", "poc_project_", False)


    #@sensitive_variables('password')
    def handle(self, request, data):
        print data
        try:
            # delete 'workflow_id' and 'workflow_name' from the param
            workflow_name = data['workflow_name']
            del data['workflow_id']
            del data['workflow_name']
            execution_id = api.nikola.workflow.launch_workflow(self.request, workflow_name, data)
            messages.success(request, _("Workflow launch started."))
            return True
        except Exception:
            exceptions.handle(request)
