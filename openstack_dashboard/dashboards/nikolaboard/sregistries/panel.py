from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.nikolaboard import dashboard

class Sregistries(horizon.Panel):
    name = _("Service Registry")
    slug = "sregistries"


dashboard.Nikolaboard.register(Sregistries)
