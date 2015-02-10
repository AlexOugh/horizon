from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.nikolaboard import dashboard

class Iams(horizon.Panel):
    name = _("IAM")
    slug = "iams"


dashboard.Nikolaboard.register(Iams)
