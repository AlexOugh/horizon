from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.nikolaboard import dashboard

class Catalogpanel(horizon.Panel):
    name = _("Service Catalog")
    slug = "catalogpanel"


dashboard.Nikolaboard.register(Catalogpanel)
