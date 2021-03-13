# movlog

movlog は個人の映画やビデオの視聴履歴を記録するツールです。

google cloud app engine 上で動作するように設計されています。

## 使用環境：

    node.js v14.11

    python 3.8

    vue 2.6.11

    vuetify 2.4.0

    pipenv version 2020.8.13

    gcloud SDK 329.0.0

## 導入準備

    googleアカウントを取得し、google cloudにプロジェクトを作成してください。


    詳細は[公式ドキュメント](https://cloud.google.com/resource-manager/docs/creating-managing-projects?hl=ja&visit_id=637504453527379254-2912142610&rd=1)を参照してください。

## プロジェクトの認証情報メニューから

    1. OAuth2.0のクライアントIDを作成
    2. 承認URIおよびコールバックURLを登録
        1. 承認URIローカルテスト用 http://localhost:5000
        2. 承認URI本番用 https://[プロジェクトのサービスURL]
        3. コールバックURL https://localhost:5000/auth/oauth2callback
        4. コールバックURL https://[プロジェクトのサービスURL]/auth/oauth2callback
        5. client_secret.jsonをダウンロード
    3. APIキーを作成し、キーを記録する
    4. google Storageを使用可能にし、movlogという名前のバケットを作成する
    5. google people APIを使用可能にする

## install

    6. client_secret.jsonをmovlogディレクトリ直下にコピーする
    7. movlog/server/secret.py.sampleを参照して server/secret.pyを作成する
    8. movlog直下で node install
    9. movlog/frontend_dev で node install
    10. movlog/server で pipenv install
    11. movlog/server/config.pyの STORAGE_LOCATIONを自分の環境に合わせて修正する
    12. npmスクリプト server/clientを起動し、ローカルでvueサーバーとpythonサーバーを起動
    13. https://localhost:5000/tables/init
    14. frontend_devのnpmスクリプトを使用して vueをビルド
