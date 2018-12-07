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
  
Python 単体で GCF 上に関数を作成した例、変数の定義方法、インポートの仕方がわかる  
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
  
GitHub API 本家、 ユーザ毎のイベント取得  
https://developer.github.com/v3/activity/events/  
  
GitHub API 本家、 レポジトリ一覧取得  
https://developer.github.com/v3/repos/#list-your-repositories  
  
GitHub API 本家、 レポジトリのコミット数を取得  
https://developer.github.com/v3/repos/commits/  
  
GitHub API 本件、クエリパラメータサンプル  
https://developer.github.com/v3/#parameters  
  
Google Cloud SDK ツール、本家  
https://cloud.google.com/sdk/docs/?hl=ja  
  
Google CLI ツール、　deploy コマンドのリファレンス  
https://cloud.google.com/sdk/gcloud/reference/functions/?hl=ja  
  
Google CLI ツール、　環境変数の定義の仕方  
https://cloud.google.com/functions/docs/env-var  
  
Google CLI ツール、　delete コマンドのリファレンス  
https://cloud.google.com/sdk/gcloud/reference/functions/delete?hl=ja  
  
スタックドライバを使ってできること  
https://www.topgate.co.jp/gcp20-what-is-stackdriver-logging  
  
Google Cloud クライアント ライブラリ 本家  
https://cloud.google.com/apis/docs/cloud-client-libraries  
  
Google Cloud クライアント ライブラリ 、Python ライブラリ、本家  
https://github.com/googleapis/google-cloud-python  
  
GCF + stackdriverサンプル、 gcf で　python を実行、 メモリ監視を stackdriver に入れる例  
https://www.apps-gcp.com/cloud-functions-python-memory-usage/  
  
Stackdriver Logging、 Python 用ロギング、リファレンス  
https://cloud.google.com/logging/docs/setup/python  
  
Stackdriver Monitoring  カスタム指標の使用  
https://cloud.google.com/monitoring/custom-metrics/?hl=ja  
  
Stackdriver Monitoring 指標、時系列、リソース  
https://cloud.google.com/monitoring/api/v3/metrics?hl=ja  
  
Stackdriver Monitoring サンプル一覧  
https://cloud.google.com/monitoring/docs/samples?hl=ja  
  
Python Stackdriver Monitoring サンプルコード  
https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/monitoring  
  
Stackdriver Monitoring Python Samples  
https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/monitoring/api/v3/api-client  
  
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
```  
curl -i -u shinonome128 https://api.github.com/repos/shinonome128/own_dashboard/traffic/popular/referrers  
```  
  
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
  
サンプルコードのコピー  
```  
cd C:\Users\shino\doc\own_dashboard  
copy accessGitHubTraffic.py get_commit_count.py  
git add *  
git commit -m "Add first commit"  
```  
  
ユーザイベント取得  
```  
GET /users/:username/events  
```  
```  
curl -i https://api.github.com/repos/shinonome128/own_dashboard/commits  
```  
これはやらない、日付指定ができないから  
  
コミット情報の取得  
動いた。。  
  
  
## レポジトリの一覧を取得  
  
利用する API  
```  
GET /users/:username/repos  
```  
```  
curl -i https://api.github.com/users/shinonome128/repos  
```  
  
取得用の関数作成  
サンプルをそのまま流用  
  
配列へ落とす  
サンプルをそのまま流用  
  
ちょっと connections と datadicts の中身が想像できないのでデバッグ  
辞書形式で特定のレコードのみを抽出して、配列に格納する処理が必要  
```  
    "id": 145781682,  
    "node_id": "MDEwOlJlcG9zaXRvcnkxNDU3ODE2ODI=",  
    "name": "detectcat",  
```  
この name のフィールドを抽出して、配列に格納する  
  
テスト  
  
コメント整形  
  
  
## 日付を生成  
  
必要なフォーマットを確認する  
```  
GET /repos/:owner/:repo/commits  
```  
```  
curl -i https://api.github.com/repos/shinonome128/own_dashboard/commits  
```  
```  
since 	string 	Only commits after this date will be returned. This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ.  
until 	string 	Only commits before this date will be returned. This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ.  
```  
```  
curl https://api.github.com/search/repositories?q=tetris+language:assembly&sort=stars&order=desc  
curl -i "https://api.github.com/repos/vmg/redcarpet/issues?state=closed"  
```  
```  
curl -i "https://api.github.com/repos/shinonome128/own_dashboard/commits?since=2018-11-23T00:00:00Z&until=2018-11-24T23:59:59Z"  
```  
  
本日の日付を生成して、9時間引く必要がある  
2018-11-23T00:00:00Z  
2018-11-24T23:59:59Z"  
  
タイムゾーンを変更  
2018-11-23T00:00:00+0900  
2018-11-23T23:59:59+0900  
```  
curl -i "https://api.github.com/repos/shinonome128/own_dashboard/commits?since=2018-11-23T00:00:00+0900&until=2018-11-23T23:59:59+0900"  
```  
  
Python での日付生成の関数サンプルを探す  
```  
datetime.date.today()  
```  
```  
datetime.datetime.now()  
```  
  
デバッグ実装  
  
コメント作成  
  
テスト  
  
## レポジトリ毎のコミット数を日付指定で取得  
  
完了  
  
## コミット数を合計  
  
関数名の修正  
  
関数の引数、 URL を修正  
  
デバッグ実装  
  
コメント作成  
  
テスト  
  
## 変数の外部ファイル化  
  
外部ファイルを GitHub 管理から外す  
```  
cd C:\Users\shino\doc\own_dashboard  
echo conf.txt>> .gitignore  
git add .gitignore  
git commit -m "Add config file"  
git push  
```  
  
外部ファイルとサンプルの作成  
トレロのの緑タグ移動のコードを参考にして作成  
```  
cd C:\Users\shino\doc\own_dashboard  
copy C:\Users\shino\doc\trello_move_green_to_plan\conf_sample.txt .\  
copy C:\Users\shino\doc\trello_move_green_to_plan\conf.txt .\  
```  
  
外部ファイルとサンプルの修正  
```  
cd C:\Users\shino\doc\own_dashboard  
copy /y conf.txt conf_sample.txt  
```  
  
デバッグ実装  
トレロのの緑タグ移動のコードを参考にして作成  
  
コメント追記  
  
テスト  
  
## ラッパーツール作成  
  
不要ファイルの削除  
```  
cd C:\Users\shino\doc\own_dashboard  
del accessGitHubTraffic.py  
git add *  
git commit -m "delete sample script"  
git push  
```  
  
WoX ラッパーの作成  
```  
cd C:\Users\shino\doc\own_dashboard  
copy C:\Users\shino\doc\trello_move_green_to_plan\move_green.bat .\get_commits.bat  
```  
  
WoX ラッパーの修正  
Puse つけること  
  
テスト  
  
## gcloud CLI ツールを使って、ディレクトリごとアップロードしてみる  
  
既存コードを GUI で GCF に移植して実行  
とりあえずコピペして実行  
ディプロイエラー  
  
主処理を　main() に変更  
環境変数から変数値を取得するように設定  
ディプロイは成功  
  
```  
トリガーのタイプ  
HTTP  
URL  
https://us-central1-gcf-demo-222516.cloudfunctions.net/function-1  
```  
トリガーのタイプ  
  
テスト  
```  
Error: could not handle the request  
```  
サンプルコードの書式に合わせてみる  
最後、 return にする  
  
curl でたたいてみる  
```  
curl -i https://us-central1-gcf-demo-222516.cloudfunctions.net/function-1  
```  
```  
HTTP/1.1 500 Internal Server Error  
Content-Type: text/plain; charset=utf-8  
X-Content-Type-Options: nosniff  
X-Cloud-Trace-Context: f1159e75f31ee2f02d6a0883e3c831ac;o=1  
Date: Fri, 23 Nov 2018 17:27:00 GMT  
Server: Google Frontend  
Content-Length: 36  
Alt-Svc: quic=":443"; ma=2592000; v="44,43,39,35"  
  
Error: could not handle the request  
```  
書き方自体が悪そう、  
GCF Python Error: could not handle the request  
で調査  
  
GCF のログを調査  
Stackdriver 経由でログが自動手的に見れるらしい  
```  
{  
 insertId: "000000-c1582708-9337-4277-a5b6-d0fcb8eb739c"  
  
labels: {…}  
 logName: "projects/gcf-demo-222516/logs/cloudfunctions.googleapis.com%2Fcloud-functions"  
 receiveTimestamp: "2018-11-23T17:27:06.988100717Z"  
  
resource: {…}  
 severity: "ERROR"  
 textPayload: "Traceback (most recent call last):  
  File "/env/local/lib/python3.7/site-packages/google/cloud/functions_v1beta2/worker.py", line 297, in run_http_function  
    result = _function_handler.invoke_user_function(flask.request)  
  File "/env/local/lib/python3.7/site-packages/google/cloud/functions_v1beta2/worker.py", line 199, in invoke_user_function  
    return call_user_function(request_or_event)  
  File "/env/local/lib/python3.7/site-packages/google/cloud/functions_v1beta2/worker.py", line 192, in call_user_function  
    return self._user_function(request_or_event)  
TypeError: main() takes 0 positional arguments but 1 was given  
"  
 timestamp: "2018-11-23T17:27:00.880Z"  
 trace: "projects/gcf-demo-222516/traces/f1159e75f31ee2f02d6a0883e3c831ac"  
}  
```  
あー、引数を最低一つは受け取らなくちゃいけないらしい  
  
main() 関数に引数を一つ指定、使わないけど  
サンプルでもかいてるね。。  
  
エラー  
```  
resource: {…}  
 severity: "ERROR"  
 textPayload: "Traceback (most recent call last):  
  File "/env/local/lib/python3.7/site-packages/google/cloud/functions_v1beta2/worker.py", line 297, in run_http_function  
    result = _function_handler.invoke_user_function(flask.request)  
  File "/env/local/lib/python3.7/site-packages/google/cloud/functions_v1beta2/worker.py", line 199, in invoke_user_function  
    return call_user_function(request_or_event)  
  File "/env/local/lib/python3.7/site-packages/google/cloud/functions_v1beta2/worker.py", line 192, in call_user_function  
    return self._user_function(request_or_event)  
  File "/user_code/main.py", line 10, in main  
    GITHUB_TOKEN = os.environ['GITHUB_REPO']  
  File "/env/lib/python3.7/os.py", line 678, in __getitem__  
    raise KeyError(key) from None  
KeyError: 'GITHUB_REPO'  
```  
あー、os.env にしたとき修正もれ、、  
  
エラー  
```  
Error: function crashed. Details:  
  
'int' object is not callable  
  
The view function did not return a valid response. The return type must be a string, tuple, Response instance, or WSGI callable, but it was a int.  
```  
リターンは必ず文字列である必要とのこと  
str() で修正  
  
動いたー、モバイルからも結果取得できたー！！  
  
手動で環境破棄  
  
## 自分ダッシュボード、gcf ディプロイ用にラップ処理  
  
デバッグ実装  
ラップ処理実装  
GCF 動作用に改造した物とマージする  
環境変数があればそのまま実行  
環境変数が無ければ、コンフィグファイルから設定を読み取って実行  
  
コメント修正  
  
テスト  
  
GCF にアップ  
  
テスト  
```  
https://us-central1-gcf-demo-222516.cloudfunctions.net/function-1  
```  
  
不要ファイルの削除  
```  
cd C:\Users\shino\doc\own_dashboard  
del test.bat  
del get_commit_count_gcf.py  
git add *  
git commit -m "Delete test file"  
git push  
```  
  
## 自分ダッシュボード、gcloud CLI ツールインスト  
  
使い方を調査  
```  
$ gcloud beta functions deploy ${YOUR_CLOUD_FUNCTION_NAME} --stage-bucket ${YOUR_STAGING_BUCKET} --trigger-http  
```  
  
インストール  
本家からバイナリをダウンロードして実行  
  
インストールディレクトリ  
```  
C:\Users\shino\AppData\Local\Google\Cloud SDK  
```  
  
WoX 起動のコマンドプロンプトだとパスが通っていないので WoX を再起動  
  
コマンド組み立て  
```  
gcloud functions deploy  
TEST  
--region=us-central1  
--runtime=python37  
--source=C:\Users\shino\doc\own_dashboard  
--trigger-http  
```  
```  
gcloud functions deploy TEST --region=us-central1 --runtime=python37 --source=C:\Users\shino\doc\own_dashboard --trigger-http  
```  
```  
C:\Users\shino\doc\own_dashboard>gcloud functions deploy TEST --region=us-central1 --runtime=python37 --source=C:\Users\shino\doc\own_dashboard --trigger-http  
Created .gcloudignore file. See `gcloud topic gcloudignore` for details.  
Deploying function (may take a while - up to 2 minutes)...failed.  
ERROR: (gcloud.functions.deploy) OperationError: code=3, message=Function load error: File main.py that is expected to define function doesn't exist  
```  
main.py である必要がある  
  
.gcloudignore に不要ファイルを追記  
```  
cd C:\Users\shino\doc\own_dashboard  
echo *swp>>.gcloudignore  
echo *txt>>.gcloudignore  
echo *bat>>.gcloudignore  
echo *md>>.gcloudignore  
echo get_commit_count.py>>.gcloudignore  
```  
  
main.py の作成  
```  
cd C:\Users\shino\doc\own_dashboard  
copy get_commit_count.py main.py  
```  
  
テスト  
```  
Deploying function (may take a while - up to 2 minutes)...failed.  
ERROR: (gcloud.functions.deploy) OperationError: code=3, message=Function load error: File main.py is expected to contain a function named TEST  
```  
揃える必要があるみたい  
  
テスト  
```  
gcloud functions deploy main --region=us-central1 --runtime=python37 --source=C:\Users\shino\doc\own_dashboard --trigger-http  
```  
ディプロイは成功  
環境変数が定義されていないので定義方法を調査  
  
環境変数の設定方法  
yml ファイルをオプション指定する  
```  
gcloud beta functions deploy FUNCTION_NAME --env-vars-file .env.yaml FLAGS...  
```  
.env.yml に記載  
```  
FOO: bar  
BAZ: boo  
```  
  
.gitignore に GCF の yml ファイルを追加  
```  
cd C:\Users\shino\doc\own_dashboard  
echo conf.yml>>.gitignore  
git add .gitignore  
git commit -m "Add conf.yml"  
git push  
```  
  
.gcloudignore にも追加  
```  
cd C:\Users\shino\doc\own_dashboard  
echo conf.yml>>.gcloudignore  
git add .gcloudignore  
git commit -m "Add conf.yml"  
git push  
```  
  
yml ファイルの作成  
```  
cd C:\Users\shino\doc\own_dashboard  
copy conf.txt conf.yml  
```  
  
conf.yml の中身を修正  
  
ディプロイ  
```  
cd C:\Users\shino\doc\own_dashboard  
gcloud functions deploy main --region=us-central1 --runtime=python37 --env-vars-file conf.yml --source=C:\Users\shino\doc\own_dashboard --trigger-http  
```  
```  
ERROR: (gcloud.functions.deploy) unrecognized arguments:  
  --env-vars-file (did you mean '--flags-file'?)  
```  
そんな引数はないと。。。あー、ベータ版コマンドだった。。  
  
ベータコマンドでディプロイ  
```  
cd C:\Users\shino\doc\own_dashboard  
gcloud beta functions deploy main --region=us-central1 --runtime=python37 --env-vars-file conf.yml --source=C:\Users\shino\doc\own_dashboard --trigger-http  
```  
```  
You do not currently have this command group installed.  Using it  
requires the installation of components: [beta]  
```  
インストしろと怒られるけお、放っておけば、勝手にインストールプロセスが始まる  
  
ディストロイ  
```  
cd C:\Users\shino\doc\own_dashboard  
gcloud beta functions delete main --region=us-central1  
```  
  
サンプル yml を作成  
```  
cd C:\Users\shino\doc\own_dashboard  
copy conf.yml conf_sample.yml  
```  
  
## 関数名 main() の修正  
  
main() を get_commit_count() に修正  
素直に変えると、最後のモジュールから呼び出されたとき main() を実行しない分に引っかかる  
やはり main() の部分には変数だけを定義するのが一番良い  
  
デバッグ実装  
  
コメント修正  
  
## ディプロイ、デストロイ用のバッチ作成  
  
ディプロイバッチ作成  
```  
cd C:\Users\shino\doc\own_dashboard  
copy get_commits.bat deploy.bat  
exit  
```  
  
deploy.bat の中身を編集  
  
ディプロイコマンド  
```  
cd C:\Users\shino\doc\own_dashboard  
gcloud beta functions deploy main --region=us-central1 --runtime=python37 --env-vars-file conf.yml --source=C:\Users\shino\doc\own_dashboard --trigger-http  
```  
  
デストロイバッチコマンド作成  
```  
cd C:\Users\shino\doc\own_dashboard  
copy get_commits.bat destroy.bat  
exit  
```  
  
destroy.bat の中身を編集  
  
デストロイコマンド  
```  
cd C:\Users\shino\doc\own_dashboard  
gcloud beta functions delete main --region=us-central1  
```  
  
テスト  
ディプロイ、実行、デストロイ  
```  
cd C:\Users\shino\doc\own_dashboard  
deploy.bat  
curl -i https://us-central1-gcf-demo-222516.cloudfunctions.net/main  
destroy.bat  
curl -i https://us-central1-gcf-demo-222516.cloudfunctions.net/main  
exit  
```  
  
## 設定ファイルごとアップロードして動作するか  
  
.gcloudignore で設定ファイルをコメントアウト  
  
deploy.bat で環境変数無しにする  
  
テスト  
ディプロイ、実行、デストロイ  
```  
cd C:\Users\shino\doc\own_dashboard  
deploy.bat  
curl -i https://us-central1-gcf-demo-222516.cloudfunctions.net/main  
destroy.bat  
curl -i https://us-central1-gcf-demo-222516.cloudfunctions.net/main  
exit  
```  
conf.txt がアップロードされていない、リクエストが速すぎた？？  
あー、main.py を削除し忘れた  
  
mail.py の削除  
```  
cd C:\Users\shino\doc\own_dashboard  
del main.py  
git add  main.py  
git commit -m "Delete main.py"  
```  
  
エラー  
```  
ERROR: (gcloud.beta.functions.deploy) OperationError: code=3, message=Function load error: File main.py that is expected to define function doesn't exist  
```  
GCF の仕様で、main.py のファイル名でなければならない  
  
ファイル名修正  
```  
cd C:\Users\shino\doc\own_dashboard  
copy get_commit_count.py main.py  
```  
  
エラー  
ディプロイは成功するけど、 conf_sample.txt がアップされてしまう  
ファイル一つの制限でもあるのかな？  
.gcloudignore に明示的に禁止して、 conf.txt をアップするようにする  
  
.gcloudignore の修正  
だめ、アップロードされない  
  
結論  
ファイル名は main.py で作成する  
main() で記載する  
main() 部分に環境変数、ファイルからの読み取り処理を入れる  
ローカル実行時は、 conf.txt から読み取る  
GCF 実行時は、 conf.yml に記載し、 環境変数から読み取る  
  
不要ファイルの削除  
```  
cd C:\Users\shino\doc\own_dashboard  
del get_commit_count.py  
```  
  
WoX ラッパーの修正  
  
コメントを修正  
  
テスト  
ローカル実行問題なし  
クラウド実行は出力が OK になっている  
リターンが定義されていない  
  
テスト  
問題なし！！  
  
## スタックドライバーにコミット数を入力  
  
  
Google Cloud クライアント ライブラリ  
Python モジュールをつかって stack driver logging にログを送信する方法を調査  
  
先にスタックドライバーと Python 実行のチュートリアルを試してみる  
```  
    名前：get-ebooks  
    割り当てるメモリ：256MB  
    トリガー：HTTP  
    ソースコード：インラインエディタ  
    ランタイム：Python3.7（ベータ版）  
    main.py：GitHub からコピー＆ペースト  
    このプログラムは、Google Books API を用いて、書籍の著者を検索キーとし、書籍のページ数が多い順にソートします。コードは以下に公開されています。  
    https://github.com/PicardParis/cloud-snippets/blob/master/python/gcf-get-ebooks/main.py  
    requirements.txt：変更なし  
    実行する関数：get_ebooks_by_author  
    リージョン：asia-northeast1  
```  
「モニタリング」をクリック  
Alerting から Create a Policy を選択  
OPT IN をクリック  
ADD CONDITION をクリック  
  
・Target  
```  
大項目 	中項目 	入力値  
Find resource type and metric 	Resource type: 	Cloud Function  
– 	Metric: 	Memory Usages  
Filter 	– 	不要  
Group By 	– 	不要  
Aggregation 	Aligner 	delta（変化量）  
– 	Reducer 	99th percentile  
Secondary Aggregation 	Reducer 	none  
```  
  
・Configuration  
```  
大項目 	中項目 	入力値  
Condition triggers if 	– 	Any time series violates  
Condition 	31457280 B ※ 	is above  
For 	– 	1 minute  
```  
  
うん、動いた。。。  
Kibana と一緒だね。  
ターゲットとコンフィギュレーションで、 ライブラリ経由でいれた、メトリクスがみれれば、このやり方でいけそうだね。  
  
google cloud クライアントの Python ライブラリのサンプル集めから開始  
  
## google cloud クライアントの Python ライブラリのサンプル集め、 stackdriver logging 連携  
  
Stackdriver Loggin Python ライブラリを利用しなくても、 GCF で実行された結果は出力がすでにロギングされている  
```  
resource.type="cloud_function"  
resource.labels.function_name="main"  
resource.labels.region="us-central1"  
textPayload="5"  
```  
なので、あとは、ダッシュボードでどのように可視化できるかだけだね。  
  
  
## Stackdriver Monitoring のダッシュボード作り方研究  
  
commit count のトリガー URL  
```  
https://us-central1-gcf-demo-222516.cloudfunctions.net/main  
```  
  
やり方  
Stackdriver Logging からログを抽出しカスタムメトリクスを作成  
カスタムメトリクスを Stackdriver Monitoring におくり自動的にチャートを作成  
  
問題  
コミットカウントがテキストフィールドなので、数値として認識されず、チャートが正常に作れない  
チャートで利用するフィールドは 数値である必要がある  
  
方針  
関数の戻り値を int にしてみる  
Stackdriver Logging Python ライブラリを利用して直接ログに送信する  
  
## 関数の戻り値を int にしてみる  
  
ブラウザでの表示ができなくなるが、スタックドライバ経由で見れれば良いので問題ないと思われる  
  
デバッグ実装  
  
ディプロイ  
```  
cd C:\Users\shino\doc\own_dashboard  
deploy.bat  
```  
  
テスト  
GUI 上から実施  
```  
Error: function crashed. Details:  
  
'int' object is not callable  
  
The view function did not return a valid response. The return type must be a string, tuple, Response instance, or WSGI callable, but it was a int.  
```  
  
関数実行後の Stackdriver logging のログエントリを調査  
関数が正常終了しないのでエントリにはトレースバックがロギングされる  
没。。。  
  
## Stackdriver Logging Python ライブラリを利用して直接ログに送信する  
  
チュートリアルに従って、API の有効化、サービスアカントの取得  
  
ライブラリのインスト  
```  
cd C:\Users\shino\AppData\Local\Programs\Python\Python36\Scripts  
pip install --upgrade google-cloud-logging  
```  
  
サンプルコード  
```  
# Imports the Google Cloud client library  
import google.cloud.logging  
  
# Instantiates a client  
client = google.cloud.logging.Client()  
  
# Connects the logger to the root logging handler; by default this captures  
# all logs at INFO level and higher  
client.setup_logging()  
```  
  
サンプルコード  
```  
# Imports Python standard library logging  
import logging  
  
# The data to log  
text = 'Hello, world!'  
  
# Emits the data using the standard logging module  
logging.warn(text)  
```  
  
デバッグ実装  
  
ローカルテスト  
エラー  
```  
google.auth.exceptions.DefaultCredentialsError: Could not automatically determine credentials. Please set GOOGLE_APPLICATION_CREDENTIALS or explicitly create credentials and re-run the application. For more information, please see https://cloud.google.com/docs/authentication/getting-started  
```  
  
Python ライブラリインストールガイドに従って、サービスアカントの作成、認証情報を取得  
  
管理対象外にする  
```  
cd C:\Users\shino\doc\own_dashboard  
echo *.json>>.gitignore  
echo *.json>>.gcloudignore  
git add .gitignore  
git add .gcloudignore  
git commit -m "Add gcp credential"  
git push  
```  
  
認証鍵をディレクトリに移動  
```  
cd C:\Users\shino\doc\own_dashboard  
move C:\Users\shino\Downloads\gcf-demo-2b39da7a07dd.json .  
```  
  
環境変数の設定  
```  
cd C:\Users\shino\doc\own_dashboard  
set GOOGLE_APPLICATION_CREDENTIALS=gcf-demo-2b39da7a07dd.json  
```  
  
ローカルテスト  
おー、うごいたーー  
  
Stackdriver のログを確認してからディプロイすること  
```  
 {  
 insertId: "3c71xfg18mty8y"  
  
jsonPayload: {  
  message: "Hello, world!"  
  python_logger: "root"  
 }  
 logName: "projects/gcf-demo-222516/logs/python"  
 receiveTimestamp: "2018-12-01T16:03:55.218686614Z"  
  
resource: {  
  
labels: {  
   project_id: "gcf-demo-222516"  
  }  
  type: "global"  
 }  
 severity: "WARNING"  
 timestamp: "2018-12-01T16:03:55.218686614Z"  
}  
```  
  
ディプロイ  
```  
cd C:\Users\shino\doc\own_dashboard  
deploy.bat  
```  
  
エラー  
```  
  File "/user_code/main.py", line 8, in <module>  
    import google.cloud.logging  
ModuleNotFoundError: No module named 'google.cloud.logging'  
```  
インポートエラー、GCF 上で pip する方法が必要、多分、 requirement.txt に書けばよいだけ  
  
requirement.txt の書き方調査  
pip freez で抽出する  
  
requirement.txt 作成  
```  
cd C:\Users\shino\doc\own_dashboard  
C:\Users\shino\AppData\Local\Programs\Python\Python36\Scripts\pip3.6.exe freeze > requirements.txt  
```  
  
.gcloudignore で テキストファイルの拡張子指定を削除して、requirements.txt がアップされるようにする  
  
エラー  
requirements.txt が多すぎて、ディプロイに時間がかかりすぎる  
```  
ERROR: (gcloud.beta.functions.deploy) OperationError: code=3, message=Build failed: Build has timed out  
```  
  
google.cloud.logging だけを追加する  
  
GCF テスト  
GUI 上から実施  
完璧、スタックドライバにきちんと Hello world がロギングされている  
  
## Stackdriver Logging のサンプルコードから、出力を変更して実装  
  
デバッグ実装  
  
ディプロイ  
```  
cd C:\Users\shino\doc\own_dashboard  
deploy.bat  
```  
  
GCFでテスト  
  
Stackdriver Logging からログを抽出しカスタムメトリクスを作成  
値を Int に指定  
  
カスタムメトリクスを Stackdriver Monitoring におくり自動的にチャートを作成  
  
Int にしたけど、なんかうまくいかん。。。  
カスタム指標の使い方、きちんとドキュメント読んで理解が必要  
  
## stackdriver loging のカスタム指標とstackdriver monitoring の使い方を調べる  
  
Logging と Monitoring のチュートリアルを探す  
ロギングした文字列から、数値を切り出して、Monitoring で数値のグラフにしているもの  
グラフは手動で作るおｔして、 Stackdriver 入門ガイドのカスタム指標の仕様 を順番にやっていけばできそう  
```  
ほとんどの指標タイプは Stackdriver Monitoring によって事前定義されていますが、ご自身で指標スキーマを定義し、データをそこに送ることによって、カスタム指標を作成することもできます。たとえば、「小売店の日別売上高」は、カスタム指標です。カスタム指標を試してみるには、カスタム指標の使用をご覧ください。  
```  
  
## サンプルコードを動かして、可視化してみる  
  
どのサンプルコードがやりたい事に一番近いか、取説を読む  
分かりやすくて量が少ないことも重要  
  
やりたい事  
GCF 上で動作して、任意の値を Stackdriver Monitoring に入れて、ダッシュボードで可視化する事  
  
サンプル  
```  
alerts-client  
api-client  
cloud-client  
uptime-check-client  
```  
  
alerts-client  
```  
This directory contains samples for Google Stackdriver Alerting API.  
```  
ちがう、アラートではなく、モニタリングのカスタム指標のコードが欲しい  
  
api-client  
```  
This directory contains samples for Stackdriver Monitoring. `  
```  
```  
""" Sample command-line program for writing and reading Stackdriver Monitoring  
API V3 custom metrics.  
Simple command-line program to demonstrate connecting to the Google  
Monitoring API to write custom metrics and read them back.  
See README.md for instructions on setting up your development environment.  
This example creates a custom metric based on a hypothetical GAUGE measurement.  
To run locally:  
    python custom_metric.py --project_id=<YOUR-PROJECT-ID>  
"""  
```  
これだ  
カスタムメトリクスに書き込み、読み込みのサンプルコード  
  
jubatus のインスタンスを起動して、コード実行してみる  
```  
python list_resources.py --project_id=jubatus-224508  
python custom_metric.py --project_id=jubatus-224508  
```  
  
コード実行結果がどのように見えるか、GCP Stackdriver Monitoring で見てみる  
Monitoring のチャート作成で、 Custom Metric が表示され、グラフが描画される  
多分この実装でけるはず!!  
  
次はコード解析と、コミットカウントのコードにマージするところから開始する  
全然会計無いけど、実行環境を勝手に作ってくれるところがクラウドシェル便利だな。何かに転用してラクできないかな。  
  
## サンプルコードの解析とマージ  
  
サンプルコードダウンロードしプロジェクトにコピー  
```  
cd C:\Users\shino\doc\own_dashboard  
git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git  
copy python-docs-samples\monitoring\api\v3\api-client\custom_metric.py .  
rmdir /s /q python-docs-samples  
```  
  
.gitignore, .gcloudignore に追加  
```  
cd C:\Users\shino\doc\own_dashboard  
echo custom_metric.py>> .gitignore  
echo custom_metric.py>> .gcloudignore  
git add *  
git commit -m "Add sample code"  
git push  
```  
  
カスタムメトリクスの作成部分を抜粋  
  
Stackdriver Monitoring への書き込み処理を追記  
  
ローカルテスト  
```  
C:\Users\shino\doc\own_dashboard>py main.py  
3  
ListCustomMetrics response:  
{'metricDescriptors': [{'description': 'An arbitrary measurement.',  
                        'displayName': 'Custom Metric',  
                        'labels': [{'description': 'An arbitrary measurement',  
                                    'key': 'environment'}],  
                        'metricKind': 'GAUGE',  
                        'name': 'projects/gcf-demo-222516/metricDescriptors/custom.googleapis.com/custom_measurement',  
                        'type': 'custom.googleapis.com/custom_measurement',  
                        'unit': 'items',  
                        'valueType': 'INT64'}]}  
  
C:\Users\shino\doc\own_dashboard>  
```  
うごいたぁー  
  
ダッシュボード作成  
  
ここから再開  
  
GCF への移植  
コード不要部分の削除  
クレデンシャルファイル名の外部変数化  
requirements.txt の作り直し  
  
EOF  
