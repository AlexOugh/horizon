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
    #kind = tables.Column("kind", verbose_name=_("Kind"))
    version = tables.Column("version", verbose_name=_("Version"))
    description = tables.Column("description", verbose_name=_("Description"))
    #documentation = tables.Column("documentation", verbose_name=_("Documentation"))
    category = tables.Column("category", verbose_name=_("Category"))

    class Meta:
        name = "registry"
        verbose_name = _("Service Registries")
        #row_actions = (LaunchCatalogLink,)
