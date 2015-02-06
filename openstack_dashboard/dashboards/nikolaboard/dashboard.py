from django.utils.translation import ugettext_lazy as _

import horizon

class Nikolagroup(horizon.PanelGroup):
    slug = "nikolagroup"
    name = _("Nikola Group")
    panels = ('workflowpanel', 'catalogpanel', 'usagepanel', )

class Nikolaboard(horizon.Dashboard):
    name = _("Nikola Board")
    slug = "nikolaboard"
    panels = (Nikolagroup,)  # Add your panels here.
    default_panel = 'workflowpanel'  # Specify the slug of the dashboard's default panel.


horizon.register(Nikolaboard)
