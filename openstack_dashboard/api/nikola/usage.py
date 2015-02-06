
import json
from django.conf import settings
from ceilometerclient import client as ceilometer_client


class Usage():
    
    def __init__(self, index, stat, meter, resource_id, resource_name):
        '''{
            "avg": 0.0,
            "count": 2,
            "duration": 20.467,
            "duration_end": "2015-01-30T19:05:54.296000",
            "duration_start": "2015-01-30T19:05:33.829000",
            "groupby": null,
            "max": 0.0,
            "meter": "disk.ephemeral.size",
            "min": 0.0,
            "period": 0,
            "period_end": "2015-01-30T19:05:33.829000",
            "period_start": "2015-01-30T19:05:33.829000",
            "project_id": "ddbfca29282841139bb7c7aa884dd579",
            "sum": 0.0,
            "unit": "GB",
            "user_id": "8a3ebabd59674ab293095d8601fa4c44"
        }'''
        self.id = str(index)
        self.avg = stat['avg']
        self.count = stat['count']
        self.duration = stat['duration']
        self.duration_end = stat['duration_end']
        self.duration_start = stat['duration_start']
        self.groupby = stat['groupby']
        self.max = stat['max']
        self.meter = meter['name']
        self.min = stat['min']
        self.period = stat['period']
        self.period_end = stat['period_end']
        self.period_start = stat['period_start']
        self.project_id = meter['project_id']
        self.sum = stat['sum']
        self.unit = stat['unit']
        self.user_id = meter['user_id']
        self.resource_id = resource_id
        self.resource_name = resource_name


def usageclient(auth_ref):
    catalog = auth_ref.get('catalog')
    endpoint = next(ep['url'] for ep in next(s['endpoints'] for s in catalog if s['name'] == 'ceilometer') if ep['interface']=='public')
    insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)
    cacert = getattr(settings, 'OPENSTACK_SSL_CACERT', None)
    return ceilometer_client.Client('2', endpoint,
                                    token=auth_ref['auth_token'],
                                    insecure=insecure,
                                    cacert=cacert)

        
def list_usages(request, search_opts=None):
    
    auth_ref = request.session['auth_ref']
    client = usageclient(auth_ref)

    vm_name = 'alex-test-1'
    vm_id = '3ba1883f-b27e-45cc-9b18-f78535ba7a2f'
    meter_query = [{'field': 'resource_id', 'type': '', 'value': vm_id, 'op': 'eq'}]

    query = []
    query.append({'field': 'resource_id', 'op': 'eq', 'value': vm_id})
    query.append({"field": "timestamp", "op": "ge", "value": "2015-01-01T00:00:00"})
    query.append({"field": "timestamp", "op": "lt", "value": "2015-02-01T00:00:00"})
    groupby = ["project_id"]
    #groupby = ["project_id", "resource_id"]
    period = None

    index = 0
    usages = []
    for meter in client.meters.list(q=meter_query):
        meter_json = meter.to_dict()
        for statistic in client.statistics.list(meter.name, q=query, period=period, groupby=groupby):
            usages.append(Usage(index, statistic.to_dict(), meter_json, vm_id, vm_name))
            #print stat
            index += 1

    has_prev_data = False
    has_more_data = False
    return (usages, has_more_data, has_prev_data)
