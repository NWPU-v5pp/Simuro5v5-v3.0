import _ctypes
import ctypes

__all__ = (
    'Converter',
    'Environment',
    'WheelInfo',
    'PlacementInfo'
)


class Converter:
    @staticmethod
    def _is_simple(_type):
        return issubclass(_type, _ctypes._SimpleCData)

    @staticmethod
    def _is_basetype(_type):
        return issubclass(_type, (int, float, str))

    @staticmethod
    def _is_array(_type):
        return issubclass(_type, _ctypes.Array)

    @staticmethod
    def _is_struct(_type):
        return issubclass(_type, _ctypes.Structure)

    @staticmethod
    def _is_dictable(_type):
        return issubclass(_type, Dictable)

    @classmethod
    def to_dict(cls, instance):
        _type = type(instance)
        if cls._is_dictable(_type):
            return instance.to_dict(instance)
        elif cls._is_basetype(_type):
            return instance
        elif cls._is_simple(_type):
            return instance.value
        elif cls._is_array(_type):
            return [cls.to_dict(sub) for sub in instance]
        elif cls._is_struct(_type):
            d = {}
            for name, _ in instance._fields_:
                sub = getattr(instance, name)
                d[name] = cls.to_dict(sub)
            return d
        else:
            return instance

    @classmethod
    def from_dict(cls, store_instance, d):
        _type = type(store_instance)
        if cls._is_dictable(_type):
            return _type.from_dict(store_instance, d)
        elif cls._is_basetype(_type):
            return d
        elif cls._is_simple(_type):
            store_instance.value = d
        elif cls._is_array(_type):
            for i, v in enumerate(d):
                store_instance[i] = cls.from_dict(store_instance[i], v)
        elif cls._is_struct(_type):
            for name, _type in store_instance._fields_:
                sub_d = d.get(name, None)  # 如果字典中没有该字段，则跳过
                if sub_d is not None:
                    sub = getattr(store_instance, name)
                    setattr(store_instance, name, cls.from_dict(sub, d[name]))

        return store_instance


class Vector3D(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_double),
        ("y", ctypes.c_double),
        ("z", ctypes.c_double)]


class Bounds(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("right", ctypes.c_long),
        ("top", ctypes.c_long),
        ("bottom", ctypes.c_long)]


class Robot(ctypes.Structure):
    _fields_ = [
        ("pos", Vector3D),
        ("rotation", ctypes.c_double),
        ("velocityLeft", ctypes.c_double),
        ("velocityRight", ctypes.c_double)]


class OpponentRobot(ctypes.Structure):
    _fields_ = [
        ("pos", Vector3D),
        ("rotation", ctypes.c_double)]


class Ball(ctypes.Structure):
    _fields_ = [("pos", Vector3D)]


class Environment(ctypes.Structure):
    _fields_ = [
        ("home", Robot * 5),
        ("opp", OpponentRobot * 5),
        ("currentBall", Ball),
        # ("lastBall", Ball),
        # ("predictedBall", Ball),
        # ("fieldBounds", Bounds),
        # ("goalBounds", Bounds),
        ("gameState", ctypes.c_int),
        ("whosBall", ctypes.c_int)
    ]


class Dictable:
    @classmethod
    def to_dict(cls, obj):
        raise NotImplementedError()

    @classmethod
    def from_dict(cls, obj, _dict):
        raise NotImplementedError()


class WheelInfo(Dictable):
    def __init__(self, dict_list=None, robot_list=None):
        if dict_list is not None:
            self.wheels = [
                {'velocityLeft': d['velocityLeft'], 'velocityRight': d['velocityRight']}
                for d in dict_list
            ]
        elif robot_list is not None:
            self.wheels = [
                {'velocityLeft': r.velocityLeft, 'velocityRight': r.velocityRight}
                for r in robot_list]
        else:
            self.wheels = [
                {'velocityLeft': 0.0, 'velocityRight': 0.0}
                for _ in range(5)
            ]

    @classmethod
    def to_dict(cls, obj):
        return {'wheels': obj.wheels}

    @classmethod
    def from_dict(cls, obj, _dict):
        obj.wheels = [
            {'velocityLeft': d['velocityLeft'], 'velocityRight': d['velocityRight']}
            for d in _dict['wheels']
        ]
        return obj


class PlacementInfo(Dictable):
    def __init__(self, env=None):
        if env is not None:
            self.robot = env.home
            self.ball = env.currentBall
        else:
            self.robot = (Robot * 5)()
            self.ball = Ball()

    @classmethod
    def to_dict(cls, obj):
        return {
            'robot': Converter.to_dict(obj.robot),
            'ball': Converter.to_dict(obj.ball)
        }

    @classmethod
    def from_dict(cls, obj, _dict):
        robots = (Robot * 5)()
        ball = Ball()
        Converter.from_dict(robots, _dict['robot'])
        Converter.from_dict(ball, _dict['ball'])
        obj.robot, obj.ball = robots, ball
        return obj


if __name__ == '__main__':
    e = Environment()
    w = WheelInfo(robot_list=e.home)
    f = PlacementInfo(env=e)
    ed = Converter.to_dict(e)
    Converter.from_dict(w, {'wheels': ed['home']})
    print(Converter.to_dict(w))
