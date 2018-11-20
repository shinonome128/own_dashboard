# README.md  
  
## 目的  
  
Check の効率化  
自分ダッシュボードの作成  
スプレッドシードでも良いので、クラウド上でコード実行、値を取得して、スマホで参照できる状態  
  
## 参照  
  
ドキュメント、コード管理  
https://github.com/shinonome128/own_dashboard  
  
サーバレスのメリット、本質、 JX 通信の小笠原さんの解説  ラップの仕方、ディプロイ、監視、可視化、CI  
https://employment.en-japan.com/engineerhub/entry/2018/07/03/110000  
  
Cloud Function 本家、 CI/CD, Clud Function エミュレータ  
https://cloud.google.com/functions/docs/bestpractices/testing  
  
Clud Function エミュレータ、本家  
https://github.com/GoogleCloudPlatform/cloud-functions-emulator/  
  
flask API ガイド  
http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response  
  
flask 超入門  
http://python.zombie-hunting-club.com/entry/2017/11/03/223503  
  
フロントにJS, バックエンドにPython を使った簡単な例、JS から Python スクリプトを実行している例、ディプロイツールでディレクトリごとアップロードする方法がわかる  
http://catindog.hatenablog.com/entry/2017/12/18/213627  
  
Python 単体で作成した例、変数の定義方法、インポートの仕方がわかる  
https://uyamazak.hatenablog.com/entry/2018/07/20/185026  
  
GitHub APIを使ってリポジトリのアクセス数をpythonで取得、単体動作で、取得API 変更するだけなのでこれで良いかも  
https://ak1211.com/3520  
https://gist.github.com/ak1211/0e21640e59c56e6c4e006ebde47c441e  
  
PHP だけど、コミット数、行数を取得するサンプル  
http://blog.koogawa.com/entry/2014/01/23/014718  
  
GitHub API 本家  
https://developer.github.com/  
  
GitHub API のアプリ登録とトークン発行方法  
https://qiita.com/ngs/items/34e51186a485c705ffdb  
  
GitHub API 本家 、Getting started、認証方法、OAuth のやり方  
https://developer.github.com/v3/guides/getting-started/  
  
GitHub パーソナルアクセストークン生成、簡単に作れる  
https://github.com/settings/tokens  
  
## やること  
  
小笠原さんのやり方で実装方法調査  
GitHub のコミット数を取得  
G ドライブのスプレッドシートに値を入力  
  
## 小笠原さんのやり方で実装方法調査  
  
サーバレス定義  
リクエストに応じて、必要なだけの計算リソースをほぼリアルタイムで確保するアーキテクチャ  
  
メリット  
リソース確保の柔軟性  
「各リクエストが確保したメモリ量で処理できるか？」であって、システム全体で確保すべきメモリに関してはあまり考える必要がありません。  
1リクエストもないときにはメモリは確保されず、費用も発生しない  
  
デメリット  
クラウド事業者の設定している上限を超えるような使い方はできません  
特定のサーバーレス環境に依存しない設計で作っておくことが重要  
  
動作  
1分間に1回、Webサービスへアクセスし、レスポンスタイムを監視する  
監視状況を、Amazon CloudWatch Metricsに保存する  
  
CloudWatch Events  
イベントに基づいて、AWSのさまざまなサービスを起動させるマネージドサービスです。Lambdaを定期的に動かします  
  
Lambda  
マネージドなFaaSです。Webサービスを監視して、その結果をCloudWatch Metricsに書き込みます  
  
CloudWatch Metrics  
メトリクスを保存して表示するマネージドサービスです。監視結果を保存します  
  
FaaSの関数をデプロイするには、次の3つの方法  
管理画面上で直接コードを書く  
公式のツール（AWS CLIなど）を使ってデプロイする  
外部のツールを使ってデプロイする、今回は、Serverless Frameworkという外部のツールを使います。  
  
Serverless Frameworkのセットアップ  
  
プロジェクトを作ります  
```  
$ serverless create --template aws-python3 --path service-watcher  
$ cd service-watcher  
```  
  
「handler.py」と「serverless.yml」という2つのファイル  
  
handler.py  
example.comにアクセスして、レスポンスが返ってくるまでにかかった時間を表示するもの  
```  
import datetime  
import urllib.request  
  
def hello(event, context):  
    started_at = datetime.datetime.now()  
    with urllib.request.urlopen("https://example.com"):  
        ended_at = datetime.datetime.now()  
        elapsed = (ended_at - started_at).total_seconds()  
        return f'Time: {elapsed} seconds'  
```  
  
ディプロイ  
```  
$ serverless deploy  
```  
AWS Lambdaの管理画面にログインすると、service-watcher-dev-helloという関数が作成されているはずです。  
  
Lambda関数の動作確認  
管理画面上で「テスト」のボタンを押してLambda関数を実行してみてください。すると実行結果が表示され、サービスのレスポンスタイムの監視ができている  
課金期間の「100 ms」は、わずか100ミリ秒のみが課金対象  
1回実行しても0.000000208円分の費用  
  
Lambda関数のテスト実行は、ターミナル上からもServerless Frameworkを使って行なうことができます。  
```  
$ serverless invoke -f hello  
"Time: 0.056416 seconds"  
```  
  
serverless.yml  
Lambda関数を定期的に実行する  
```  
functions:  
  hello:  
    handler: handler.hello  
    events:  
      - schedule: rate(1 minute)  
```  
  
再度、デプロイ  
```  
$ serverless deploy  
```  
管理画面を確認してみると、左側にCloudWatch Eventsが追加され、スケジュール式のところに「rate(1 minute)」と表示  
  
監視結果を保存する  
監視の結果をCloudWatch Metricsに書き込みます。  
handler.pyを変更  
```  
import datetime  
import urllib.request  
import boto3  
  
def hello(event, context):  
    cloudwatch = boto3.client('cloudwatch')  
    started_at = datetime.datetime.now()  
    with urllib.request.urlopen("https://example.com"):  
        ended_at = datetime.datetime.now()  
        elapsed = (ended_at - started_at).total_seconds()  
        cloudwatch.put_metric_data(  
            Namespace='Watcher',  
            MetricData=[{  
                'MetricName': 'ResponseTime',  
                'Unit': 'Milliseconds',  
                'Value': elapsed,  
                'Dimensions': [  
                    {'Name': 'URL', 'Value': 'https://example.com'}  
                ]  
            }]  
        )  
```  
  
デプロイして、実行  
```  
$ serverless deploy  
$ serverless invoke -f hello  
```  
  
```  
{  
    "errorMessage": "An error occurred (AccessDenied) when calling the PutMetricData operation(略)",  
    ...  
}  
```  
今デプロイしたAWS Lambdaが、CloudWatch Metricsに対して書き込みをする権限を持っていないために起きているエラーです  
  
serverless.ymlを変更  
Lambda関数にCloudWatch Metricsに書き込むための権限を与えます。  
iamRoleStatements:以下の行が今回の変更分です  
Lambda関数のソースコード内のcloudwatch.put_metric_dataという処理に権限が足りていなかったので、cloudwatch:PutMetricDataの権限を許可  
```  
provider:  
  name: aws  
  runtime: python3.6  
  iamRoleStatements:  
    - Effect: "Allow"  
      Action:  
       - "cloudwatch:PutMetricData"  
      Resource: "*"  
```  
  
再度、デプロイと実行  
```  
$ serverless deploy  
$ serverless invoke -f hello  
```  
  
CloudWatch Metricsの管理画面を開き、メトリクス→Watcher→URL→ResponseTimeと選択してみてください。すると、以下のようにグラフが作られています  
サーバーレスにWebサービスの監視を定期的に行い、結果を保存してグラフが見られるようになりました。  
  
監視の結果、異常があればSlackへアラートを投げるといったシステムへ発展させることもできます。  
サーバーレスなシステムの設計を突き詰めていくと、マネージドサービスを組み合わせ、イベントドリブンで各サービスが発火していくような設計になります。  
  
コードをより良くしてみる〜ローカル環境での実行  
  
handler.pyは、AWS Lambdaの環境で動くことしか想定していないコード  
watcher.pyというファイルを作って、次のようにコードを書き換えてみます。  
```  
# watcher.py  
import datetime  
import urllib.request  
import boto3  
  
def watch(url):  
    cloudwatch = boto3.client('cloudwatch')  
    started_at = datetime.datetime.now()  
    with urllib.request.urlopen(url):  
        # 略  
  
# `python watcher.py https://example.com`と実行できる  
if __name__ == '__main__':  
    import sys  
    watch(sys.argv[1])  
```  
```  
# handler.py  
import wacher  
# Lambdaはこの関数を呼び出す  
def hello(event, context):  
    watcher.watch("https://example.com")  
```  
この設計の場合、今まで通りLambda上でも動き、ローカル環境でpython watcher.py [url]することでも動作できます。  
ローカルで動くCLIツールを、Lambdaでも動くようにラップするような設計  
Lambdaはあくまでデプロイする先の環境の一つであるという捉え方をして開発する  
別のサーバーレス環境やPaaSへ移行したり、サーバーレスをやめることも簡単  
  
サーバーレスアプリケーションの継続的な開発  
Apexなどのいくつかのオープンソースなツールが存在します。ApexにはTerraformとの連携ができるメリットがある  
CIでの自動テストをどのように行うのかという問題も出てきます。テスタビリティを高めるという観点でも、特定のクラウドサービス依存しないようにプログラムを設計することが重要  
マネージドサービスへのアクセスを含むシステムをテストする際には、localstackのような「マネージドサービスのモックをしたもの」を使うと、クラウドの利用費がかからず、テストに使ったリソースの破棄も容易なので便利  
  
サーバーレスでの課題〜システムの監視と管理  
「複数の小さなシステムを組み合わせたときの監視をどうしていくか？」という点が運用の課題  
AWSでは、公式の監視ツールとして、Amazon CloudWatchと、AWS X-ray  
Amazon CloudWatchは、AWSの各サービスのログやメトリクスを表示  
AWS X-rayは複数システムの連携という観点から、プロファイリングが行える  
サーバーレスなシステムの設計をもっと大規模にすると、マネージドサービスが複雑に絡み合って管理が大変になっていく傾向にあります。  
管理の観点からも、Serverless Frameworkのようなツールの利用を前提とすると良い  
  
## サービスと外部ツールの検討  
  
CloudWatch Events  
イベントトリガーは今回は使わない  
GCF の HTTP トリガーで十分  
  
Lambda  
GCF を使う  
  
CloudWatch Metrics  
メトリクスの格納先と可視化  
stack driver を使う  
  
外部のツール  
ディプロイ管理  
terraform を使う  
  
モック環境  
マネージドサービスのモックをしたもの  
Cloud Functions エミュレータ  
  
CI ツール  
次のステップ、今回はやらない  
  
## GitHub のコミット数を取得  
  
チュートリアルコードの解析  
```  
def hello_world(request):  
    """Responds to any HTTP request.  
    Args:  
        request (flask.Request): HTTP request object.  
    Returns:  
        The response text or any set of values that can be turned into a  
        Response object using  
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.  
    """  
    request_json = request.get_json()  
    if request.args and 'message' in request.args:  
        return request.args.get('message')  
    elif request_json and 'message' in request_json:  
        return request_json['message']  
    else:  
        return f'Hello World!'  
```  
flask API に従って記載するらしい  
HTTP トリガーで処理ができればよいので、、  
  
フロントにJS, バックエンドにPython を使った簡単な例  
JS から Python スクリプトを実行している  
ディプロイツールでディレクトリごとアップロードするには、dcloud ツール使っている  
```  
# index.js  
const spawnSync = require('child_process').spawnSync;  
exports.reflection = function reflection(req, res) {  
  result = spawnSync('./pypy3-v5.9.0-linux64/bin/pypy3', ['./reflection.py'], {  
    stdio: 'pipe',  
    input: JSON.stringify(req.headers)  
  });  
  if (result.stdout){  
    res.status(200).send(result.stdout);  
  }else if (result.stderr){  
    res.status(200).send(result.stderr);  
  }  
};  
```  
```  
# reflection.py  
import json  
print(json.dumps(json.loads(input()), indent=2))  
```  
  
Python 単体での実装方法、この方法で良いかも  
Python 単体で作成した例、変数の定義方法、インポートの仕方がわかる  
```  
import feedparser  
import json  
RSS_URL = "https://blog.yagish.jp/rss"  
WHITELIST = ['http://192.168.2.70:2105', 'http://ml30gen9.jp:2105', 'https://rirekisho.yagish.jp']  
MAX_ENTRIES_NUM = 3  
  
def rss2json(request):  
    headers = {}  
    origins = [val for key, val in request.headers if key == 'Origin']  
    if len(origins) > 0:  
        origin = origins[0]  
        for allowed_url in WHITELIST:  
            if origin == allowed_url:  
                headers['Access-Control-Allow-Origin'] = allowed_url  
                break  
    headers["Content-Type"] = "application/json; charset=utf-8"  
    headers["Cache-Control"] = "public, max-age=30, s-maxage=60"  
    rss = {}  
    try:  
        raw_rss = feedparser.parse(RSS_URL)  
        rss['feed'] = raw_rss['feed']  
        rss['entries'] = raw_rss['entries'][:MAX_ENTRIES_NUM]  
    except Exception(e):  
        return (e, 500)  
    else:  
        return (json.dumps(rss, indent=2, ensure_ascii=False),  
                headers)  
```  
  
GitHub APIを使ってリポジトリのアクセス数をpythonで取得  
単体動作で、取得API 変更するだけなのでこれで良いかも  
```  
#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
import os, json, functools  
from urllib2 import urlopen, Request  
  
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
print "\n".join (dumps)  
```  
  
とりあえずサンプルを動かしてみる  
```  
cd C:\Users\shino\doc\own_dashboard  
git clone https://gist.github.com/0e21640e59c56e6c4e006ebde47c441e.git  
copy 0e21640e59c56e6c4e006ebde47c441e\accessGitHubTraffic.py .\  
rmdir /s /q 0e21640e59c56e6c4e006ebde47c441e  
```  
```  
cd C:\Users\shino\doc\own_dashboard  
set GITHUB_TOKEN=hoge  
set GITHUB_OWNER=shinonome128  
set GITHUB_REPO=own_dashboard  
py accessGitHubTraffic.py  
```  
  
エラー  
```  
Traceback (most recent call last):  
  File "accessGitHubTraffic.py", line 4, in <module>  
    from urllib2 import urlopen, Request  
ModuleNotFoundError: No module named 'urllib2'  
```  
urllib2 がない、調査  
  
Python3系でurllib2は使えない：代わりにurllib.requestとurllib.errorを使う  
```  
import urllib.request, urllib.error  
```  
  
エラー  
```  
  File "accessGitHubTraffic.py", line 15, in openTrafficAPI  
    return urlopen (Request (url, headers=headers))  
NameError: name 'urlopen' is not defined  
```  
urlopen がこのままだと使えない、調査  
  
urllib2.urlopen は urllib.request.urlopen() に変更  
```  
Python 2.6 以前のレガシーな urllib.urlopen 関数は廃止されました。  
urllib.request.urlopen() が過去の urllib2.urlopen に相当します。  
urllib.urlopen において辞書型オブジェクトで渡していたプロキシの扱いは、ProxyHandler オブジェクトを使用して取得できます。  
```  
  
エラー  
```  
  File "accessGitHubTraffic.py", line 14, in openTrafficAPI  
    return urlopen (Request (url, headers=headers))  
NameError: name 'Request' is not defined  
```  
Request がインポートされてない、 urllib.request.Request() となるので、urlopen と同じ対処が必要  
  
エラー  
```  
urllib.error.HTTPError: HTTP Error 401: Unauthorized  
```  
認証エラー、あー、クレデンシャル適当だった  
  
クレデンシャル直してもダメ  
デバッグで URL をブラウザでたたいて確認  
```  
(Pdb) url  
https://api.github.com/repos/shinonome128/own_dashboard/traffic/popular/referrers  
```  
ブラウザでの確認結果  
```  
{  
  "message": "Must have push access to repository",  
  "documentation_url": "https://developer.github.com/v3/repos/traffic/#list-referrers"  
}  
```  
プッシュがない、URL 見ろとのこと  
  
プッシュアクセスしてから実施  
効果なし  
  
URL見てみる  
```  
List referrers  
Get the top 10 referrers over the last 14 days.  
  
GET /repos/:owner/:repo/traffic/popular/referrers  
  
Response  
  
Status: 200 OK  
  
[  
  {  
    "referrer": "Google",  
    "count": 4,  
    "uniques": 3  
  },  
  {  
    "referrer": "stackoverflow.com",  
    "count": 2,  
    "uniques": 2  
  },  
  {  
    "referrer": "eggsonbread.com",  
    "count": 1,  
    "uniques": 1  
  },  
  {  
    "referrer": "yandex.ru",  
    "count": 1,  
    "uniques": 1  
  }  
]  
```  
URL は間違っていない、  
  
  
メッセージ調査  
Must have push access to repository  
```  
For repositories that you have push access to, the traffic API provides access to the information provided in the graphs section.  
```  
参照先の API リファレンスガイドにプッシュアクセスが必須って書いてある。。。  
あー、トークンの発行が必要なんだね、多分  
  
ベークック認証だとうまくいく  
curl -i -u shinonome128 https://api.github.com/repos/shinonome128/own_dashboard/traffic/popular/referrers  
  
アクセストークンを取得して実行  
エラー  
```  
urllib.error.HTTPError: HTTP Error 400: Bad Request  
```  
認証は治ったけど、今度はリクエスト不正、、、あー、環境変数のセットで余分が空白が入っていた。。  
  
動いた。。  
```  
C:\Users\shino\doc\own_dashboard>py accessGitHubTraffic.py  
[]  
[]  
{  
  "count": 0,  
  "uniques": 0,  
  "views": []  
}  
{  
  "count": 1,  
  "uniques": 1,  
  "clones": [  
    {  
      "timestamp": "2018-11-18T00:00:00Z",  
      "count": 1,  
      "uniques": 1  
    }  
  ]  
}  
  
C:\Users\shino\doc\own_dashboard>  
```  
  
## サンプルコードを参考にコミット数を取得する  
  
ここから再開  
  
  
以上  
