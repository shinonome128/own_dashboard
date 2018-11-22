import os, json, functools
from urllib.request import urlopen, Request
from datetime import datetime

## レポジトリ情報取得関数
def get_repository (owner, token):
    url = "https://api.github.com/users/%s/repos" % (owner)
    headers = {
        'Authorization': 'token %s' % token,
        'Accept': 'application/vnd.github.spiderman-preview'
    }
    return urlopen (Request (url, headers=headers))

connections = []
try:
    # レポジトリ情報を取得
    connections = get_repository(
                                os.environ['GITHUB_OWNER'],
                                os.environ['GITHUB_TOKEN'])
    # JSONパース
    datadicts = json.loads (connections.read ())

finally:
    # 後始末
    [c.close () for c in connections if c is not None]

del connections

# レポジトリ名一覧の取得
repo = []
for i in datadicts:
    for k, v in i.items():
        if k == 'name':
            repo.append(v)

# コミット情報取得関数
def get_commit (owner, token, since, until, repo):
    url = "https://api.github.com/repos/%s/%s/commits?since=%s&until=%s" % (owner, repo, since, until)
    headers = {
        'Authorization': 'token %s' % token,
        'Accept': 'application/vnd.github.spiderman-preview'
    }
    return urlopen (Request (url, headers=headers))

connections = []
try:
    ## コミット情報を取得、部分的に変数を組み立て
    fAPI = functools.partial (get_commit,
                                os.environ['GITHUB_OWNER'],
                                os.environ['GITHUB_TOKEN'],
                                str(datetime.now())[0:10]+'T00:00:00+0900',
                                str(datetime.now())[0:10]+'T23:59:59+0900')
    # open connections
    connections = [fAPI (r) for r in repo]
    # JSONパース
    datadicts = [json.loads (c.read ()) for c in connections]

finally:
    # 後始末
    [c.close () for c in connections if c is not None]

del connections

# コミット回数の取得
commit_counts = 0
for i in datadicts:
    if len(i) > 0:
        for j in i:
            for k in j.keys():
                if k == 'sha':
                    commit_counts += 1

## 回数を表示
print(commit_counts)
