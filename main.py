import os, json, functools
from urllib.request import urlopen, Request
from datetime import datetime
import configparser
import codecs
import googleapiclient.discovery
import time

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

    # Set stackdriver monitoring param
    project_id = "gcf-demo-222516"
    CUSTOM_METRIC_DOMAIN = "custom.googleapis.com"
    CUSTOM_METRIC_TYPE = "{}/CommitCounts".format(CUSTOM_METRIC_DOMAIN)
    project_resource = "projects/{0}".format(project_id)
    client = googleapiclient.discovery.build('monitoring', 'v3')

    # Write commit counts to stackdriver monitoring
    write_timeseries_value(client, project_resource, CUSTOM_METRIC_TYPE, commit_counts)

    # dashboard url
    line = "<iframe src=\"https://public.google.stackdriver.com/public/chart/3264884998933248819?drawMode=color&showLegend=true&theme=dark&timeframe=1w\" width=\"800\" height=\"400\" scrolling=\"no\" seamless=\"seamless\"></iframe>"

    # Display dashboard url
    return line 

# Write commits counts to stackdriver monitoring
def write_timeseries_value(client, project_resource, custom_metric_type, commit_counts):
    now = get_now_rfc3339()
    timeseries_data = {
        "metric": {
            "type": custom_metric_type,
            "labels": {
                "environment": "STAGING"
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


# Get time
def get_now_rfc3339():
    return format_rfc3339(datetime.utcnow())


# Change time format
def format_rfc3339(datetime_instance=None):
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
