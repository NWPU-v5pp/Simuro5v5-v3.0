class SucceedExit(Exception):
    # 正常退出
    exit_code = 0


class UnknownException(Exception):
    # Message错误
    exit_code = 1


class DllException(Exception):
    # dll错误
    pass

class PlatFormExitedException(Exception):
    # 平台退出
    exit_code = 3
