
import json
from django.conf import settings
from ceilometerclient import client as ceilometer_client


class Workbook():
    
    def __init__(self, workbook_json):
        '''{
            "definition": "---\\nversion: '2.0'\\nname: nikola_poc_sample_alex\\n\\nworkflows:\\n customer_setup:\\n description: Setup a new customer by creating domain/project/admin_user\\n type: direct\\n input:\\n - requester_sso_token\\n - root_op_user_name\\n - root_op_password\\n - root_op_domain_name\\n - email\\n - first_name\\n - last_name\\n - password\\n - company_uuid\\n - auth_url\\n - domain_name\\n - domain_description\\n - project_name\\n - project_description\\n - enabled\\n output:\\n# sso_uuid: $.sso_uuid\\n auth_admin_url: $.auth_admin_url\\n token: $.token\\n domain_id: $.domain_id\\n project_id: $.project_id\\n user_id: $.user_id\\n\\n tasks:\\n create_user_in_sso:\\n action: nikola.serviceAction_sync target='iam' method='create_user_in_sso' requester_sso_token={$.requester_sso_token} email={$.email} first_name={$.first_name} last_name={$.last_name} password={$.password} company_uuid={$.company_uuid} project_name={$.project_name}\\n publish:\\n sso_uuid: $.create_user_in_sso.sso_uuid\\n on-success:\\n - authenticate_in_openstack \\n\\n authenticate_in_openstack:\\n action: nikola.serviceAction_sync target='openstack' method='authenticate' auth_url={$.auth_url} user_name={$.root_op_user_name} password={$.root_op_password} domain_name={$.root_op_domain_name}\\n publish:\\n auth_admin_url: $.authenticate_in_openstack.auth_admin_url\\n token: $.authenticate_in_openstack.token\\n on-success:\\n - create_domain_in_openstack\\n\\n create_domain_in_openstack:\\n action: nikola.serviceAction_sync target='openstack' method='create_domain' domain_name={$.domain_name} description={$.domain_description} enabled={$.enabled} auth_admin_url={$.auth_admin_url} admin_token={$.token}\\n publish:\\n domain_id: $.create_domain_in_openstack.id\\n on-success:\\n - create_project_in_openstack\\n\\n create_project_in_openstack:\\n action: nikola.serviceAction_sync target='openstack' method='create_project' project_name={$.project_name} description={$.project_description} enabled={$.enabled} domain_id={$.domain_id} auth_admin_url={$.auth_admin_url} admin_token={$.token}\\n publish:\\n project_id: $.create_project_in_openstack.id\\n on-success:\\n - create_user_in_openstack\\n\\n create_user_in_openstack:\\n action: nikola.serviceAction_sync target='openstack' method='create_user' user_name={$.email} email={$.email} password={$.password} enabled={$.enabled} domain_id={$.domain_id} auth_admin_url={$.auth_admin_url} admin_token={$.token}\\n publish:\\n user_id: $.create_user_in_openstack.id\\n on-success:\\n - add_admin_role_to_user_in_openstack\\n\\n add_admin_role_to_user_in_openstack:\\n action: nikola.serviceAction_sync target='openstack' method='add_admin_role_to_user' user_id={$.user_id} domain_id={$.domain_id} auth_admin_url={$.auth_admin_url} admin_token={$.token}\\n on-success:\\n - associate_project_to_user_in_openstack\\n\\n associate_project_to_user_in_openstack:\\n action: nikola.serviceAction_sync target='openstack' method='associate_project_to_user' project_id={$.project_id} user_id={$.user_id} auth_admin_url={$.auth_admin_url} admin_token={$.token}\\n on-success:\\n - store_user_info_to_iam\\n\\n store_user_info_to_iam:\\n action: nikola.serviceAction_sync target='iam' method='store_user_info' sso_uuid={$.sso_uuid} email={$.email} first_name={$.first_name} last_name={$.last_name} password={$.password} company_uuid={$.company_uuid} project_name={$.project_name}\\n publish:\\n sso_uuid: $.store_user_info_to_iam.sso_uuid\\n",
            "name": "nikola_poc_sample_alex",
            "tags": [ ],
            "created_at": "2015-02-06 15:55:16",
            "updated_at": null,
            "scope": "private",
            "id": "4d25f69b-3ead-4bac-954e-c13aa392c06f"
        }'''
        self.id = workbook_json['id']
        self.name = workbook_json['name']
        self.tags = workbook_json['tags']
        self.created_at = workbook_json['created_at']
        self.updated_at = workbook_json['updated_at']
        self.scope = workbook_json['scope']
        self.definition = workbook_json['definition']


def list_workbooks(request, search_opts=None):
    
    from nikola_api import NikolaAPI
    nikapi = NikolaAPI()
    res = nikapi.send(url='/useast1/nikola/r2/workflow/list_workbooks', data='{"all":null}')
    print 'result = %s' % res['result']
    workbooks = []
    for workbook in res['result']['result']['workbooks']:
        workbooks.append(Workbook(workbook))

    has_prev_data = False
    has_more_data = False
    return (workbooks, has_more_data, has_prev_data)


def list_workflows(request, search_opts=None):
    
    from nikola_api import NikolaAPI
    nikapi = NikolaAPI()
    res = nikapi.send(url='/useast1/nikola/r2/workflow/list_workflows', data='{"all":null}')
    print 'result = %s' % res['result']
    workbooks = []
    for workbook in res['result']['result']['workbooks']:
        workbooks.append(Workbook(workbook))

    has_prev_data = False
    has_more_data = False
    return (workbooks, has_more_data, has_prev_data)
