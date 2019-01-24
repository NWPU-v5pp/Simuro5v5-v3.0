import json
from data_structure import *
import logging


class MessageType:
    # 相同的typestr只有一个实例，作为msg的类型
    _types = {}

    def __new__(cls, typestr):
        # 查找已有的实例
        t = cls._types.get(typestr, None)
        if t is not None:
            return t
        else:
            return super().__new__(cls)

    def __init__(self, type_name: str):
        self.type = type_name
        self._types[type_name] = self

    def __repr__(self):
        return '<MessageType: {}>'.format(self.type)

    def __str__(self):
        return '<MessageType: {}>'.format(self.type)


# 定义不同的Message类型
MSG_true = MessageType('true')
MSG_false = MessageType('false')
MSG_ping = MessageType('ping')
MSG_pong = MessageType('pong')
MSG_error = MessageType('error')
MSG_load = MessageType('load')
MSG_free = MessageType('free')
MSG_create = MessageType('create')
MSG_strategy = MessageType('strategy')
MSG_placement = MessageType('placement')
MSG_destroy = MessageType('destroy')
MSG_placementinfo = MessageType('placementinfo')
MSG_wheelinfo = MessageType('wheelinfo')
MSG_exit = MessageType('exit')
MSG_fin = MessageType('fin')


# Message的容器，存储Message以及相对应的数据
class MsgAny:
    # 任意数据

    def __init__(self, msgtype: MessageType, _dict: dict):
        self.msg_type = msgtype
        self.data = _dict

    def to_dict(self):
        if self.data is None:
            return {'type': self.msg_type.type}
        else:
            return {'type': self.msg_type.type, 'data': self.data}


class MsgNoData(MsgAny):
    # 无数据容器

    def __init__(self, msgtype: MessageType, _dict: dict):
        super().__init__(msgtype, _dict)
        self.msg_type = msgtype
        self.data = _dict


class MsgEnv(MsgAny):
    # 存储Environment的容器

    def __init__(self, msgtype: MessageType, _dict: dict, env: Environment = None):
        super().__init__(msgtype, _dict)
        self.msg_type = msgtype
        self.data = None
        if _dict is not None:
            self.data = _dict
            struct = Environment()
            self.env = Converter.from_dict(struct, _dict)
        elif env is not None:
            self.env = env
            self.data = Converter.to_dict(env)


class MsgFile(MsgAny):
    # 存储文件信息的容器

    def __init__(self, msgtype: MessageType, _dict: dict, filename: str = None):
        super().__init__(msgtype, _dict)
        self.msg_type = msgtype
        self.data = None
        if _dict is not None:
            self.data = _dict
            self.filename = _dict['filename'] if _dict['filename'] != None else ""
        elif filename is not None:
            self.filename = filename
            self.data = {'filename': filename}


class MsgWheelInfo(MsgAny):
    # 存储5个轮子信息

    def __init__(self, msgtype: MessageType, _dict: dict, wheelinfo: WheelInfo = None):
        super().__init__(msgtype, _dict)
        self.msg_type = msgtype
        self.data = None
        if _dict is not None:
            self.data = _dict
            self.wheelinfo = WheelInfo()
            Converter.from_dict(self.wheelinfo, _dict)
        elif wheelinfo is not None:
            self.wheelinfo = wheelinfo
            self.data = Converter.to_dict(self.wheelinfo)


class MsgPlacementInfo(MsgAny):
    # 摆位信息

    def __init__(self, msgtype: MessageType, _dict: dict, placementinfo: PlacementInfo = None):
        super().__init__(msgtype, _dict)
        self.msg_type = msgtype
        if _dict is not None:
            self.data = _dict
            self.placementinfo = Converter.from_dict(
                PlacementInfo(), _dict)
        elif placementinfo is not None:
            self.placementinfo = placementinfo
            self.data = Converter.to_dict(placementinfo)


class MsgError(MsgAny):
    # 错误

    def __init__(self, msgtype, _dict, errcode=-1, errdesc=None):
        super().__init__(msgtype, _dict)
        self.msg_type = msgtype
        if _dict is not None:
            self.data = _dict
            self.errcode = _dict['errcode']
            self.errdesc = str(_dict['errdesc'])
        else:
            self.data = {'errcode': errcode, 'errdesc': str(errdesc)}
            self.errcode = errcode
            self.errdesc = str(errdesc)


# 记录Message类型字符串到类型实例以及对应容器的映射
_message_map = {}


def register_msg(msgtype: MessageType, _class: type):
    _message_map[msgtype.type] = (msgtype, _class)


def msg_from_json(j: str) -> MsgAny:
    try:
        d = json.loads(j)
    except Exception as ex:
        raise TypeError("error message: " + str(ex))

    typestr = d.get('type', None)
    if typestr is None:
        raise TypeError("error message")
    if typestr not in _message_map:
        raise TypeError("unknown message type")

    data = d.get('data', None)
    msgtype = _message_map[typestr][0]
    return make_msg(msgtype, _dict=data)


def msg_to_json(msg: MsgAny) -> str:
    if msg.data is None:
        return json.dumps(msg.to_dict())
    else:
        return json.dumps(msg.to_dict())


def make_msg(msgtype, _dict, **kwargs) -> MsgAny:
    # _dict为消息字典中data字段的字典内容
    # kwargs会传递给相应的消息容器
    return _message_map[msgtype.type][1](msgtype, _dict, **kwargs)


register_msg(MSG_true, MsgNoData)
register_msg(MSG_false, MsgNoData)
register_msg(MSG_free, MsgNoData)
register_msg(MSG_exit, MsgNoData)
register_msg(MSG_ping, MsgNoData)
register_msg(MSG_pong, MsgNoData)
register_msg(MSG_load, MsgFile)
register_msg(MSG_create, MsgEnv)
register_msg(MSG_strategy, MsgEnv)
register_msg(MSG_placement, MsgEnv)
register_msg(MSG_destroy, MsgEnv)
register_msg(MSG_wheelinfo, MsgWheelInfo)
register_msg(MSG_placementinfo, MsgPlacementInfo)
register_msg(MSG_error, MsgError)
register_msg(MSG_fin, MsgNoData)

if __name__ == '__main__':
    e = Environment()
    wd = Converter.to_dict(e.home)
    wm = make_msg(MSG_wheelinfo, {'wheels': wd})
    fd = {'robot': Converter.to_dict(e.home), 'ball': Converter.to_dict(e.currentBall)}
    fm = make_msg(MSG_placementinfo, fd)
    print(fm.to_dict())
