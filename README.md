# discordMCbot
WebArena Indigoと連動して、コマンドからサーバーを起動するdiscordのbotです。

Indigoが従量課金制なので、サーバー代の節約に使えます。

# Feature
discordから、Indigoの起動、Minecraftサーバーの起動ができます。

# Requirement
* python3.10以上
* その他、requirements.txtに記載

# Installation
```bash
pip install -r requirements.txt
```

# Usage
設定ファイル`config.ini`を、自分の環境に合ったものに変更

[INDIGO]

Indigoのサイトから取得
* API_ID: IndigoのAPI_ID
* API_SECRET_KEY: IndigoのAPI_SECRET_KEY


[INSTANCE]

こちらも、Indigoのサイトから情報取得
* MC_INSTANCE_NAME: マイクラサーバーとして利用するインスタンスの名前
* address: マイクラサーバーとして利用するインスタンスのIP(ssh接続でそうさするため必要)
* user_name: マイクラサーバーとして利用するインスタンスのuser_name
* identity_file: マイクラサーバーとして利用するインスタンスの秘密鍵ファイルのパス

[MCRCON]
* address: マイクラサーバーのIPアドレス
* password: マイクラサーバーのrconのパスワード(server.propertiesのなかにrcon.passwordがあるのでそれに合わせる。)
* port: マイクラサーバーのrconのポート。デフォルトのままであれば変更不要

[DISCORD]
* token: discord botのトークン