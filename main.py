import os, json, functools
from urllib.request import urlopen, Request
from datetime import datetime
import configparser
import codecs

# Add Stackdriver monitoring write
import googleapiclient.discovery
import time
import pprint

# Read environment variables and settings
def main(request = ''):
    try:
        # Get parameters from environment variables
        GITHUB_OWNER = os.environ['GITHUB_OWNER']
        GITHUB_TOKEN = os.environ['GITHUB_TOKEN']

    except:
        # Load configuration file
        conf_file = 'conf.txt'
        config = configparser.ConfigParser()

        # Open configuration file
        config.readfp(codecs.open(conf_file, "r", "utf8"))

        # Read parameters
        GITHUB_OWNER = config.get('API', 'GITHUB_OWNER')
        GITHUB_TOKEN = config.get('API', 'GITHUB_TOKEN')
        GOOGLE_APPLICATION_CREDENTIALS = config.get('API', 'GOOGLE_APPLICATION_CREDENTIALS')
        
        # Set env
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS

    # Get_commit_counts
    commit_counts = get_commit_count(GITHUB_OWNER, GITHUB_TOKEN)

    # Display commit counts
    print(commit_counts)

    # [START write to stackdriver monitoring]
    # This is the project id
    project_id = "gcf-demo-222516"
    # This is the namespace for all custom metrics
    CUSTOM_METRIC_DOMAIN = "custom.googleapis.com"
    # This is our specific metric name
    CUSTOM_METRIC_TYPE = "{}/custom_measurement".format(CUSTOM_METRIC_DOMAIN)
    INSTANCE_ID = "test_instance"
    METRIC_KIND = "GAUGE"

    project_resource = "projects/{0}".format(project_id)
    client = googleapiclient.discovery.build('monitoring', 'v3')
    # create_custom_metric(client, project_resource,
    #                     CUSTOM_METRIC_TYPE, METRIC_KIND)
    custom_metric = None
    while not custom_metric:
        # wait until it's created
        time.sleep(1)
        custom_metric = get_custom_metric(
            client, project_resource, CUSTOM_METRIC_TYPE)

    write_timeseries_value(client, project_resource,
                           CUSTOM_METRIC_TYPE, INSTANCE_ID, METRIC_KIND, commit_counts)
    # [END write to stackdriver monitoring]

    # Return commit counts
    return str(commit_counts)


# Add Stackdriver monitoring write
def create_custom_metric(client, project_id,
                         custom_metric_type, metric_kind):
    """Create custom metric descriptor"""
    metrics_descriptor = {
        "type": custom_metric_type,
        "labels": [
            {
                "key": "environment",
                "valueType": "STRING",
                "description": "An arbitrary measurement"
            }
        ],
        "metricKind": metric_kind,
        "valueType": "INT64",
        "unit": "items",
        "description": "An arbitrary measurement.",
        "displayName": "Custom Metric"
    }

    return client.projects().metricDescriptors().create(
        name=project_id, body=metrics_descriptor).execute()


# Add Stackdriver monitoring write
def get_custom_metric(client, project_id, custom_metric_type):
    """Retrieve the custom metric we created"""
    request = client.projects().metricDescriptors().list(
        name=project_id,
        filter='metric.type=starts_with("{}")'.format(custom_metric_type))
    response = request.execute()
    print('ListCustomMetrics response:')
    pprint.pprint(response)
    try:
        return response['metricDescriptors']
    except KeyError:
        return None


# Add Stackdriver monitoring write
# [START write_timeseries]
def write_timeseries_value(client, project_resource,
                           custom_metric_type, instance_id, metric_kind, commit_counts):
    """Write the custom metric obtained by get_custom_data_point at a point in
    time."""
    # Specify a new data point for the time series.
    now = get_now_rfc3339()
    timeseries_data = {
        "metric": {
            "type": custom_metric_type,
            "labels": {
                "environment": "STAGING"
            }
        },
        "resource": {
            "type": 'gce_instance',
            "labels": {
                'instance_id': instance_id,
                'zone': 'us-central1-f'
            }
        },
        "points": [
            {
                "interval": {
                    "startTime": now,
                    "endTime": now
                },
                "value": {
                    "int64Value": commit_counts
                }
            }
        ]
    }

    request = client.projects().timeSeries().create(
        name=project_resource, body={"timeSeries": [timeseries_data]})
    request.execute()
# [END write_timeseries]


# Add Stackdriver monitoring write
def get_now_rfc3339():
    # Return now
    return format_rfc3339(datetime.utcnow())


# Add Stackdriver monitoring write
def format_rfc3339(datetime_instance=None):
    """Formats a datetime per RFC 3339.
    :param datetime_instance: Datetime instanec to format, defaults to utcnow
    """
    return datetime_instance.isoformat("T") + "Z"


# Calculate commit counts
def get_commit_count(GITHUB_OWNER, GITHUB_TOKEN):

    connections = []
    try:
        # Get repository informations
        connections = get_repository(
                                    GITHUB_OWNER,
                                    GITHUB_TOKEN)

        # Perse json
        datadicts = json.loads (connections.read ())

    finally:
        # Cleanup
        [c.close () for c in connections if c is not None]

    del connections

    # Get repository name list
    repo = []
    for i in datadicts:
        for k, v in i.items():
            if k == 'name':
                repo.append(v)

    connections = []
    try:
        # Get commit informations, partially assembling variables
        fAPI = functools.partial (get_commit,
                                    GITHUB_OWNER,
                                    GITHUB_TOKEN,
                                    str(datetime.now())[0:10]+'T00:00:00+0900',
                                    str(datetime.now())[0:10]+'T23:59:59+0900')
        # open connections
        connections = [fAPI (r) for r in repo]
        # Perse json
        datadicts = [json.loads (c.read ()) for c in connections]

    finally:
        # Cleanup
        [c.close () for c in connections if c is not None]

    del connections

    # Get commit counts
    commit_counts = 0
    for i in datadicts:
        if len(i) > 0:
            for j in i:
                for k in j.keys():
                    if k == 'sha':
                        commit_counts += 1

    return commit_counts


# Repository information acquisition function
def get_repository (owner, token):
    url = "https://api.github.com/users/%s/repos" % (owner)
    headers = {
        'Authorization': 'token %s' % token,
        'Accept': 'application/vnd.github.spiderman-preview'
    }
    return urlopen (Request (url, headers=headers))


# Commit information acquisition function
def get_commit (owner, token, since, until, repo):
    url = "https://api.github.com/repos/%s/%s/commits?since=%s&until=%s" % (owner, repo, since, until)
    headers = {
        'Authorization': 'token %s' % token,
        'Accept': 'application/vnd.github.spiderman-preview'
    }
    return urlopen (Request (url, headers=headers))


# Execute main() only when you call it directly
if __name__ == "__main__":
    main()
