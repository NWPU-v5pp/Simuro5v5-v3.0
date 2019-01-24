from data_structure import *
from exception import *
import ctypes
import _ctypes
import message
import logging
import socket
import argparse
import time
import threading
import os
import sys
from pathlib import PureWindowsPath


class Strategy:
    dll = None
    dll_path = None
    functions = ("Create", "Strategy", "Destroy", "Placement")

    def __init__(self, dll_path):
        if not os.path.isabs(dll_path):
            dll_path = str(PureWindowsPath(os.getcwd(), dll_path))
        else:
            dll_path = str(PureWindowsPath(dll_path))

        logging.info("Initializing Strategy " + dll_path)

        self.dll_path = dll_path
        self.dll = ctypes.cdll.LoadLibrary(self.dll_path)
        self.check_dll()

    def check_dll(self):
        logging.info("checking dll")

        if self.dll is None:
            raise DllException('no dll loaded')
        for func in self.functions:
            if getattr(self.dll, func, None) is None:
                msg = "func `{}` is not in dll {}".format(func, self.dll_path)
                logging.error(msg)
                raise DllException(msg)

    def free(self):
        _ctypes.FreeLibrary(self.dll._handle)

    def dll_create(self, env):
        if self.dll is None:
            logging.error("no dll loaded")
            raise DllException("no dll loaded")

        logging.info("Executing `Create()` func")
        self.dll.Create(ctypes.pointer(env))

    def dll_strategy(self, env):
        if self.dll is None:
            logging.error("no dll loaded")
            raise DllException("no dll loaded")

        logging.info("Executing `Strategy()` func")
        self.dll.Strategy(ctypes.pointer(env))

    def dll_placement(self, env):
        if self.dll is None:
            logging.error("no dll loaded")
            raise DllException("no dll loaded")

        self.dll.Placement(ctypes.pointer(env))

    def dll_destroy(self, env):
        if self.dll is None:
            logging.error("no dll loaded")
            raise DllException("no dll loaded")

        logging.info("Executing `Destroy()` func")
        self.dll.Destroy(ctypes.pointer(env))


class MsgConn:
    def send_msg(self, msg):
        raise NotImplementedError

    def recv_msg(self):
        raise NotImplementedError

    def wait_client(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class TCPMsgConn(MsgConn):

    def __init__(self, address, port):
        self.peer_endpoint = None
        self.conn = None
        self.listen_endpoint = (address, port)
        self._listen_sock = socket.socket()
        self._listen_sock.bind(self.listen_endpoint)
        self._listen_sock.listen(10)

    def int_to_bytes(self, i):
        return int.to_bytes(i, 2, 'big')

    def bytes_to_int(self, bs):
        return int.from_bytes(bs, 'big')

    def wait_client(self):
        self.conn, self.peer_endpoint = self._listen_sock.accept()
        logging.warning("client connected " + str(self.peer_endpoint))
        logging.warning("closing listen socket")
        self._listen_sock.close()

    def send_msg(self, msg):
        if self.conn is None:
            raise Exception("not connected yet")
        data = message.msg_to_json(msg).encode("utf8")
        size = len(data)
        self.conn.sendall(self.int_to_bytes(size) + data)

    def recv_msg(self):
        if self.conn is None:
            raise Exception("not connected yet")
        size = self.bytes_to_int(self.conn.recv(2))
        data = self.conn.recv(size)
        return message.msg_from_json(data.decode('utf8'))

    def close(self):
        self.conn.close()


class UDPMsgConn(MsgConn):
    _udp_buffer_size = 10240

    def __init__(self, address, port):
        self.self_endpoint = (address, port)
        self.peer_endpoint = None
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.conn.bind(self.self_endpoint)

    def wait_client(self):
        pass

    def send_msg(self, msg):
        if self.peer_endpoint is None:
            raise Exception("client not connected yet")
        self.conn.sendto(message.msg_to_json(msg).encode('utf8'), self.peer_endpoint)

    def recv_msg(self):
        data, ep = self.conn.recvfrom(self._udp_buffer_size)
        if self.peer_endpoint is None:
            # 记录第一个发送消息的客户端
            self.peer_endpoint = ep
            logging.warning("client connected " + str(self.peer_endpoint))
        if ep != self.peer_endpoint:
            raise Exception("unexcepted client " + str(ep) + ". Excepting " + str(self.peer_endpoint))
        return message.msg_from_json(data.decode('utf8'))

    def close(self):
        self.conn.close()


class MessageHandler:
    handler_map = {}
    conn = None
    client_endpoint = None
    strategy = None

    def __init__(self, conn: MsgConn):
        self.handler_map[message.MSG_load] = self.handle_load
        self.handler_map[message.MSG_free] = self.handle_free
        self.handler_map[message.MSG_ping] = self.handle_ping
        self.handler_map[message.MSG_create] = self.handle_create
        self.handler_map[message.MSG_strategy] = self.handle_strategy
        self.handler_map[message.MSG_placement] = self.handle_placement
        self.handler_map[message.MSG_destroy] = self.handle_destroy
        self.handler_map[message.MSG_exit] = self.handle_exit
        self.conn = conn

    def handle(self):
        logging.info("waiting for message")
        while True:
            msg = self.conn.recv_msg()
            logging.info("handling message: " + str(msg.msg_type))

            if msg.msg_type not in self.handler_map:
                edesc = "not excepted message type " + str(msg.msg_type)
                logging.error(edesc)
                self.send_error(-1, edesc)
            self.handler_map[msg.msg_type](msg)

    def send_fin(self):
        self.conn.send_msg(message.make_msg(message.MSG_fin, None))

    def send_error(self, errcode, errdesc):
        msg = message.make_msg(message.MSG_error, None, errcode=errcode, errdesc=errdesc)
        self.conn.send_msg(msg)

    def handle_ping(self, msg):
        logging.info('get ping, replying pong')
        self.conn.send_msg(message.make_msg(message.MSG_pong, None))

    def handle_load(self, msg):
        logging.info('get load message, loading dll ' + msg.filename)
        if self.strategy is not None:
            logging.info('removing last dll ' + self.strategy.dll_path)
            self.strategy.free()

        try:
            self.strategy = Strategy(msg.filename)
        except Exception as ex:
            logging.error(ex)
            self.send_error(0, str(ex))
        else:
            self.send_fin()

    def handle_free(self, msg):
        if self.strategy is not None:
            logging.info('freeing dll ' + self.strategy.dll_path)
            self.strategy.free()
            self.strategy = None
            self.send_fin()
        else:
            logging.info('no dll loaded')
            self.send_error(0, "no dll loaded")

    def handle_create(self, msg):
        if self.strategy is None:
            emsg = 'no dll loaded'
            logging.error(emsg)
            self.send_error(0, emsg)
        else:
            logging.info("executing func `Create`")
            self.strategy.dll_create(msg.env)
            self.send_fin()

    def handle_strategy(self, msg):
        if self.strategy is None:
            emsg = 'no dll loaded'
            logging.error(emsg)
            self.send_error(0, "no dll loaded")
        else:
            logging.info("executing func `Strategy`")
            self.strategy.dll_strategy(msg.env)
            wheelinfo = WheelInfo(robot_list=msg.env.home)
            respmsg = message.make_msg(message.MSG_wheelinfo, None, wheelinfo=wheelinfo)
            self.conn.send_msg(respmsg)

    def handle_placement(self, msg):
        if self.strategy is None:
            emsg = 'no dll loaded'
            logging.error(emsg)
            self.send_error(0, emsg)
        else:
            logging.info("executing func `Placement`")
            self.strategy.dll_placement(msg.env)
            finfo = PlacementInfo(env=msg.env)
            respmsg = message.make_msg(message.MSG_placementinfo, None, placementinfo=finfo)
            self.conn.send_msg(respmsg)

    def handle_destroy(self, msg):
        if self.strategy is None:
            emsg = 'no dll loaded'
            logging.error(emsg)
            self.send_error(0, emsg)
        else:
            logging.info("executing func `Destroy`")
            self.strategy.dll_destroy(msg.env)
            self.send_fin()

    def handle_exit(self, msg):
        logging.info('exiting...')
        self.send_fin()
        exit()


def notice_lock_file(lockpath):
    logging.info("noticing platform lock file")

    def f():
        while os.path.exists(lockpath):
            time.sleep(1)
        logging.error("Platform has exited. Exiting...")
        os._exit(PlatFormExitedException.exit_code)

    threading.Thread(target=f, daemon=True).start()


def main():
    parser = argparse.ArgumentParser(description='Strategy Server')
    parser.add_argument('-p', '--port', dest='port', type=int,
                        action='store', help='Listen port.')
    parser.add_argument('--log-file', dest='log_file',
                        action='store', help='File to output log.')
    parser.add_argument('--log-append', dest='log_append',
                        action='store_true', help='write log with append mode')
    parser.add_argument('--udp', dest='udp',
                        action='store_true', help='use udp to communicate')
    parser.add_argument('--lock-file', dest='lock_file',
                        action='store', help='server exit if lock_file missing.')
    args = parser.parse_args()

    # logging settings
    log_format = '[%(asctime)s] %(levelname)s (%(funcName)s:%(lineno)s) - %(message)s'
    log_level = logging.DEBUG
    if args.log_append:
        log_mode = 'a'
    else:
        log_mode = 'w'
    if args.log_file is not None:
        logging.basicConfig(filename=args.log_file, filemode=log_mode, level=log_level, format=log_format)
    else:
        logging.basicConfig(level=log_level, format=log_format)

    # port settings
    if args.port is None:
        raise TypeError('no port')

    # lock file settings
    if args.lock_file is not None:
        notice_lock_file(args.lock_file)

    logging.warning("pid: {}, ppid: {}".format(os.getpid(), os.getppid()))

    # connect settings
    if args.udp:
        logging.warning("new udp waiting on " + str(("localhost", args.port)))
        conn = UDPMsgConn("localhost", args.port)
        logging.warning("waiting client connection...")
    else:
        logging.warning("new tcp listening on " + str(("localhost", args.port)))
        conn = TCPMsgConn("localhost", args.port)
        logging.warning("waiting client connection...")
        conn.wait_client()
        logging.warning("client connected " + str(conn.peer_endpoint))

    try:
        msg_handler = MessageHandler(conn)
        msg_handler.handle()
    finally:
        logging.warning("shuting socket down")
        conn.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        logging.error(ex)
        exit_code = getattr(ex, 'exit_code', UnknownException.exit_code)
        sys.exit(exit_code)
