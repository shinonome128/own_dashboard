# README.md  
  
## 目的  
  
Check の効率化  
自分ダッシュボードの作成  
スプレッドシードでも良いので、クラウド上でコード実行、値を取得して、スマホで参照できる状態  
  
## 参照  
  
ドキュメント、コード管理  
https://github.com/shinonome128/own_dashboard  
  
サーバレスのメリット、本質、 JX 通信の小笠原さんの解説  
https://employment.en-japan.com/engineerhub/entry/2018/07/03/110000  
  
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
  
ここから再開  
  
  
  
## サービスと外部ツールの検討  
  
CloudWatch Events  
Lambda  
CloudWatch Metrics  
外部のツール  
  
## GitHub のコミット数を取得  
  
## G ドライブのスプレッドシートに値を入力  
  
以上  
