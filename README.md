# acsu-login
acsuネットワークに自動ログインするためのpythonスクリプト
## 依存環境の構築
- windows
    - opensslをインストール  
    [ここ](https://slproweb.com/products/Win32OpenSSL.html)から自身のコンピュータのビット数にあった, 
    なるべく新しいものをインストールしてパスを通す
    - pythonをインストール  
    \ cmdなどで`python -V` を実行してエラーが出なければ必要ない.
    ただし, インタプリタのパッケージマネージャからrequestsをインストールすること.   
    \ エラーが出るならば,  [ここ](https://www.python.org)からpythonをインストール
    pathはpython.exeに加えて, pipにも通す.
    `pip install requests`を実行する.
    
- ubuntu  
opensslをインストール    
` apt install openssl`  
pythonモジュール *requests*のインストール  
`pip3 install requests`  

## 使用方法
すべてコマンドラインから実行する.
windowsの場合, .pyファイルをpythonと紐づけておけば, 
設定を使ったログインがされるため, クリックひとつで事は足りる.
- 初期設定  
` python acsu.py init`
- 設定リセット  
` python acsu.py reset`
- 設定を使ってログイン  
` python acsu.py `
- 設定を使わずログイン  
` python acsu.py login`
