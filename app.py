from wsgiref.simple_server import make_server
from wsgiref.util import FileWrapper
import json, yaml, codecs, os, inspect, smbus, time

# インストールルートディレクトリ取得
irdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

remote_controller_dir = '/remote-controller/remote-controller/'

ext = '.yaml'
hk9493 = {}

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This must match in the Arduino Sketch
#SLAVE_ADDRESS = 0x04
SLAVE_ADDRESS = 0x52
data_numH     = 0x31
data_numL     = 0x32
data_numHL    = [0x00,0x31,0x32]
data_num      = 10
memo_no       = 0
block         = []

#command
R1_memo_no_write  = 0x15  #bus-write(ADR,cmd,1)
R2_data_num_read  = 0x25 #bus-read(ADR,cmd,3)
R3_data_read      = 0x35 #bus-read(ADR,cmd,n)
W1_memo_no_write  = 0x19 #bus-write(ADR,cmd,1)
W2_data_num_write = 0x29 #bus-write(ADR,cmd,3)
W3_data_write     = 0x39 #bus-read(ADR,cmd,n)
W4_flash_write    = 0x49 #bus-read(ADR,cmd,n)
T1_trans_start    = 0x59 #bus-write(ADR,cmd,1)

# リモコンデータのロード
def load_remocon_data():
    # 呼び出し元の関数名をリモコンデータ名とする
    mname = inspect.currentframe().f_back.f_code.co_name
    return load_remocon_data_internal(mname)

# リモコンデータのロード
def load_remocon_data_internal(kiki):
    with codecs.open(irdir + remote_controller_dir + kiki + ext, 'r', 'utf-8') as fs:
        rdata = yaml.safe_load(fs)
        return rdata

# 機器コード指定してリモコン情報取得
def get_rdata(kiki):
    return load_remocon_data_internal(kiki)

def HK9493():
    return load_remocon_data()

# #############trans command
def trans_command(block2):
    #f = open(filename,'r')
    #block2 =f.read()
    #f.close()
    #print(block2)
    #print(len(block2))
    str_tmp = ""
    int_tmp = []
    for i in range(int(len(block2)//2)):
    #for i in range(len(block2)/2):
        str_tmp = block2[i*2] + block2[i*2+1]
        int_tmp.append( int(str_tmp, 16))
    #print(int_tmp)  
    #print(len(int_tmp))
# cmd W2_data_num_write 0x29 bus-write(ADR,cmd,3)
    data_num = int(len(int_tmp)//4)  #for test
    data_numHL = [0x31,0x32] #for test
    data_numHL[0] = int(data_num//256)
    data_numHL[1] = int(data_num%256)
    bus.write_i2c_block_data(SLAVE_ADDRESS, W2_data_num_write ,  data_numHL)   #= 
# cmd W3_data_write           0x39 bus-read(ADR,cmd,n)
    #print(data_num)
    data_numHL = [0x31,0x32,0x33,0x34] #for test 
    for i in range(data_num):
         data_numHL[0] = int_tmp[i*4+0]
         data_numHL[1] = int_tmp[i*4+1]
         data_numHL[2] = int_tmp[i*4+2]
         data_numHL[3] = int_tmp[i*4+3]
         bus.write_i2c_block_data(SLAVE_ADDRESS, W3_data_write , data_numHL)   #= 
 # cmd T1_trans_start             0x59 bus-write(ADR,cmd,1)
    memo_no = [0x00 ] #for dummy
    bus.write_i2c_block_data(SLAVE_ADDRESS, T1_trans_start,memo_no )   #= 

def application(environ, start_response):
    path = environ['PATH_INFO']

    if path == '/':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return render('./index.html', environ, start_response)
    elif path == '/css/main.css':
        start_response('200 OK', [('Content-Type', 'text/css')])
        return render('./css/main.css', environ, start_response)
    elif path == '/js/main.js':
        start_response('200 OK', [('Content-Type', 'text/javascript')])
        return render('./js/main.js', environ, start_response)
    elif path == '/hk9493/akarui':
        return control_hk9493('akarui', environ, start_response)
    elif path == '/hk9493/atatakaiiro':
        return control_hk9493('atatakaiiro', environ, start_response)
    elif path == '/hk9493/jouyatou':
        return control_hk9493('jouyatou', environ, start_response)
    elif path == '/hk9493/kurai':
        return control_hk9493('kurai', environ, start_response)
    elif path == '/hk9493/shiroiiro':
        return control_hk9493('shiroiiro', environ, start_response)
    elif path == '/hk9493/shoutou':
        return control_hk9493('shoutou', environ, start_response)
    elif path == '/hk9493/tentou':
        return control_hk9493('tentou', environ, start_response)
    elif path == '/hk9493/zentou':
        return control_hk9493('zentou', environ, start_response)
        
    start_response('200 OK', [('Content-type', 'application/json')])
    return [json.dumps({'message':'Not Found'}).encode("utf-8")]

def control_hk9493(operator, environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/javascript')])
    trans_command(hk9493[operator])
    time.sleep(0.05) # 0.05秒以下だと反応しないことがある
    return [json.dumps({'message':operator}).encode("utf-8")]

def render(file_path, environ, start_response):
    return FileWrapper(open(file_path, 'rb'))

def init_adrsir():
    global hk9493
    hk9493 = HK9493()
    print("Initialize ADRSIR.")

with make_server('', 3000, application) as httpd:
    init_adrsir()
    print("Serving on port 3000...")
    httpd.serve_forever()