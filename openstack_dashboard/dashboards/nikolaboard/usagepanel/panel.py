from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.nikolaboard import dashboard

class Usagepanel(horizon.Panel):
    name = _("Usage")
    slug = "usagepanel"


dashboard.Nikolaboard.register(Usagepanel)
