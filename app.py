from wsgiref.simple_server import make_server

import json, yaml, codecs, os, inspect

# インストールルートディレクトリ取得
irdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

remote_controller_dir = '/light-controller/remote-controller/'

ext = '.yaml'

# リモコンデータのロード
def load_remocon_data():
    # 呼び出し元の関数名をリモコンデータ名とする
    mname = inspect.currentframe().f_back.f_code.co_name
    return load_remocon_data_internal(mname)

# リモコンデータのロード
def load_remocon_data_internal(kiki):
    with codecs.open(irdir + remote_controller_dir + kiki + ext, 'r', 'utf-8') as fs:
        rdata = yaml.load(fs)
        return rdata

# 機器コード指定してリモコン情報取得
def get_rdata(kiki):
    return load_remocon_data_internal(kiki)

def HK9493():
    return load_remocon_data()

def app(environ, start_response):
    status = '200 OK'
    headers = [
        ('Content-type', 'application/json; charset=utf-8'),
        ('Access-Control-Allow-Origin', '*'),
    ]
    start_response(status, headers)

    return [json.dumps({'message':'hoge'}).encode("utf-8")]

def init_adrsir():
    print("Initialize ADRSIR.")

with make_server('', 3000, app) as httpd:
    rdata = HK9493()
    print(rdata['zentou'])
    print("Serving on port 3000...")
    httpd.serve_forever()