import os, json, functools
from urllib.request import urlopen, Request

## レポジトリ情報取得
def get_repository (owner, token):
    url = "https://api.github.com/users/%s/repos" % (owner)
    headers = {
        'Authorization': 'token %s' % token,
        'Accept': 'application/vnd.github.spiderman-preview'
    }
    return urlopen (Request (url, headers=headers))

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

## 日付を生成、あとでやる

## コミット情報取得
def openTrafficAPI (owner, token, repo):
    ## 日付を取得してパラメータで渡す、後でやる
    url = "https://api.github.com/repos/%s/%s/commits" % (owner, repo)
    headers = {
        'Authorization': 'token %s' % token,
        'Accept': 'application/vnd.github.spiderman-preview'
    }
    return urlopen (Request (url, headers=headers))

connections = []
try:
    # openTrafficAPI関数の部分適用 (認証情報を環境変数から得て)
    # 日付情報も後で渡す、あとでやる
    fAPI = functools.partial (openTrafficAPI,
                                os.environ['GITHUB_OWNER'],
                                os.environ['GITHUB_TOKEN'])
    # open connections
    connections = [fAPI (r) for r in repo]
    # JSONパース
    datadicts = [json.loads (c.read ()) for c in connections]
finally:
    [c.close () for c in connections if c is not None]          # 後始末

del connections

# 辞書型のデーターをダンプ
dumps = [json.dumps (d, indent=2) for d in datadicts]

# 結合
print ("\n".join (dumps))
