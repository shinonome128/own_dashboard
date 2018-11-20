#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, json, functools
# from urllib2 import urlopen, Request
from urllib.request import urlopen, Request

# GitHub Traffic API
# https://developer.github.com/v3/repos/traffic/
def openTrafficAPI (owner, repo, token, path):
    url = "https://api.github.com/repos/%s/%s/traffic/%s" % (owner, repo, path)
    headers = {
        'Authorization': 'token %s' % token,
        'Accept': 'application/vnd.github.spiderman-preview'
    }
    return urlopen (Request (url, headers=headers))

# 取ってくるデーター
paths = [
    'popular/referrers',
    'popular/paths',
    'views',
    'clones',
]

connections = []
try:
    # openTrafficAPI関数の部分適用 (認証情報を環境変数から得て)
    fAPI = functools.partial (openTrafficAPI,
                                os.environ['GITHUB_OWNER'],
                                os.environ['GITHUB_REPO'],
                                os.environ['GITHUB_TOKEN'])

    import pdb; pdb.set_trace()

    # open connections
    connections = [fAPI (p) for p in paths]
    # JSONパース
    datadicts = [json.loads (c.read ()) for c in connections]
finally:
    [c.close () for c in connections if c is not None]          # 後始末

del connections

# 辞書型のデーターをダンプ
dumps = [json.dumps (d, indent=2) for d in datadicts]
# 結合
print ("\n".join (dumps))
