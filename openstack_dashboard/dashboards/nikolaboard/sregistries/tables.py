from django.utils.translation import ugettext_lazy as _

from horizon import tables


'''class LaunchCatalogLink(tables.LinkAction):
    name = "create"
    verbose_name = _("Launch Service Catalog")
    url = "horizon:nikolaboard:catalogpanel:launch"

    def allowed(self, request, user):
        return True'''


class RegistryTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"), link="horizon:nikolaboard:sregistries:detail")
    #status = tables.Column("description", verbose_name=_("Description"))
    #zone = tables.Column('availability', verbose_name=_("Availability"))

    class Meta:
        name = "registry"
        verbose_name = _("Service Registries")
        #row_actions = (LaunchCatalogLink,)
