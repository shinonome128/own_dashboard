import os, json, functools
from urllib.request import urlopen, Request
from datetime import datetime
import configparser
import codecs

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

    # get_commit_count(GITHUB_OWNER, GITHUB_TOKEN)
    commit_counts = get_commit_count(GITHUB_OWNER, GITHUB_TOKEN)

    # Display commit counts
    print(commit_counts)

    # Return commit counts
    # return str(commit_counts)
    return commit_counts

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
