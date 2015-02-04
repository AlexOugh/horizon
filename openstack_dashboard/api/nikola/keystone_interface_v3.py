
#from os import environ as env
import simplejson as json
from django.utils.translation import ugettext_lazy as _
import keystoneclient.v2_0.client as ksclient
from keystone_v3 import KeystoneV3
from keystoneclient import exceptions as keystone_exceptions

def authenticate(auth_url, user_name, password, domain_name):

    from keystoneclient.v3 import client as client_v3
    
    insecure = False
    ca_cert = None
    endpoint_type = 'publicURL'
    #user_domain_name = 'default'
    #username = 'admin'
    #password = 'password'
    #auth_url = 'http://172.20.1.50:5000/v3/'
    
    try:
        client = client_v3.Client(
            user_domain_name=domain_name,
            username=user_name,
            password=password,
            auth_url=auth_url,
            insecure=insecure,
            cacert=ca_cert,
            debug=False)
    except (keystone_exceptions.Unauthorized,
            keystone_exceptions.Forbidden,
            keystone_exceptions.NotFound) as exc:
        msg = _('Invalid user name or password.')
        raise Exception(msg)
    except (keystone_exceptions.ClientException,
            keystone_exceptions.AuthorizationFailure) as exc:
        msg = _("An error occurred authenticating. "
                "Please try again later.")
        raise Exception(msg)

    unscoped_auth_ref = client.auth_ref
    
    client.management_url = auth_url
    try:
        #projects = [p.to_dict() for p in client.projects.list(user=client.auth_ref.user_id)]
        projects = client.projects.list(user=client.auth_ref.user_id)
    except (keystone_exceptions.ClientException,
            keystone_exceptions.AuthorizationFailure) as exc:
        msg = _('Unable to retrieve authorized projects.')
        raise Exception(msg)

    if not projects:
        msg = _('You are not authorized for any projects.')
        raise Exception(msg)

    while projects:
        project = projects.pop()
        try:
            client = client_v3.Client(
                tenant_id=project.id,
                token=client.auth_ref.auth_token,
                auth_url=auth_url,
                insecure=insecure,
                cacert=ca_cert,
                debug=False)
            auth_ref = client.auth_ref
            break
        except (keystone_exceptions.ClientException,
                keystone_exceptions.AuthorizationFailure):
            auth_ref = None

    if auth_ref is None:
        msg = _("Unable to authenticate to any available projects.")
        raise Exception(msg)

    return (unscoped_auth_ref, auth_ref, client.service_catalog)


def get_client(auth_admin_url, admin_token):
    # auth_admin_url = 'http://controller:35357/v2.0'   # instead of port 5000
    keystone = ksclient.Client(endpoint=auth_admin_url, token=admin_token)
    return keystone


def create_tenant(tenant_name, description, enabled, auth_admin_url, admin_token):
    """tenant_name = "openstackDemo"
    description = "Default Tenant"
    enabled = True"""
    keystone = get_client(auth_admin_url, admin_token)
    tenant = keystone.tenants.create(tenant_name=tenant_name, description=description, enabled=enabled)
    print tenant
    return tenant.to_dict()


def list_tenants(auth_admin_url, admin_token):
    keystone = get_client(auth_admin_url, admin_token)
    tenants = []
    for tenant in keystone.tenants.list():
        tenants.append(tenant.to_dict())
    print tenants
    return tenants


def create_user(user_name, password, tenant_name, auth_admin_url, admin_token):
    """user_name = "adminUser"
    password = "secretword"
    tenant_name = "openstackDemo"
    """
    keystone = get_client(auth_admin_url, admin_token)
    tenants = keystone.tenants.list()
    my_tenant = [x for x in tenants if x.name==tenant_name][0]
    my_user = keystone.users.create(name=user_name, password=password, tenant_id=my_tenant.id)
    print my_user
    return my_user.to_dict()


def list_users(auth_admin_url, admin_token):
    keystone = get_client(auth_admin_url, admin_token)
    users = []
    for user in keystone.users.list():
        users.append(user.to_dict())
    print users
    return users


def list_roles(auth_admin_url, admin_token):
    keystone = get_client(auth_admin_url, admin_token)
    roles = keystone.roles.list()
    print roles
    return roles


##### failed!!!
##### keystoneclient.openstack.common.apiclient.exceptions.Conflict: Conflict occurred attempting to store role - Duplicate Entry (HTTP 409)
def add_user_role(user_name, tenant_name, role_name, auth_admin_url, admin_token):
    """user_name = "adminUser"
    tenant_name = "second"
    role_name = "_member_"
    """
    keystone = get_client(auth_admin_url, admin_token)
    role = keystone.roles.create(role_name)
    tenants = keystone.tenants.list()
    my_tenant = [x for x in tenants if x.name==tenant_name][0]
    users = keystone.users.list()
    my_user = [x for x in users if x.name==user_name][0]
    keystone.roles.add_user_role(my_user, role, my_tenant)


