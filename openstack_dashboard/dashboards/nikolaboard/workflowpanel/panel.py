from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.nikolaboard import dashboard

class Workflowpanel(horizon.Panel):
    name = _("Workflow")
    slug = "workflowpanel"


dashboard.Nikolaboard.register(Workflowpanel)
