# 全局库 etp
# 用于定义错误类型
    # 例如 ConfigError

from .etp import ConfigError, EnvError

__all__ = ["ConfigError", "EnvError"]
