class ConfigError(Exception):
    """配置文件加载失败"""
    pass

class EnvError(Exception):
    """环境变量文件加载失败"""
    pass
