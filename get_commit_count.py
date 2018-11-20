import os, json, functools
from urllib.request import urlopen, Request

def openTrafficAPI (owner, token, repo):
    ## 日付を取得してパラメータで渡す、後でやる
    url = "https://api.github.com/repos/%s/%s/commits" % (owner, repo)
    headers = {
        'Authorization': 'token %s' % token,
        'Accept': 'application/vnd.github.spiderman-preview'
    }
    return urlopen (Request (url, headers=headers))

## レポジトリの一覧を取得して配列に格納、あとでやる

repo = [
    'own_dashboard',
    'autologin',
    'cicddemo',
    'detectcat',
    'devops-example-client',
    'devops-example-server',
    'gcptest',
    'gvim',
    'gwcheck',
    'jr',
    'knowledge',
    'lteanalysis',
    'own_dashboard',
    'trello_move_green_to_clip',
    'trello_move_green_to_plan',
    ]

## 日付を生成、あとでやる

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
