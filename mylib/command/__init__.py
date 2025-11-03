# 用于定义指令
    # 例如 /ping <msg>

# 启发于 GNU/Linux


from .parser import CommandParser
from .registry import registry
from .decorators import simple_command, command, argument


registry.auto_import()

__all__ = ["CommandParser", "registry", "simple_command", "command", "argument"]
