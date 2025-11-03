class RedError(Exception):
    """带红色输出的基础错误"""
    def __str__(self):
        return f"\033[31m{super().__str__()}\033[0m"


class ConfigError(RedError):
    """配置文件加载失败"""
    pass


class EnvError(RedError):
    """环境变量文件加载失败"""
    pass
