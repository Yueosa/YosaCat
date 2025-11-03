from typing import Dict, Callable
from .base import CommandMeta


class CommandRegistry:
    def __init__(self):
        self.simple_commands: Dict[str, Callable] = {}
        self.advanced_commands: Dict[str, CommandMeta] = {}

    def register_simple(self, name, func):
        self.simple_commands[name] = func

    def register_advanced(self, meta: CommandMeta):
        self.advanced_commands[meta.name] = meta

    def get_advanced(self, name: str):
        return self.advanced_commands.get(name)

    def auto_import(self):
        """
        自动导入 CAD.commands 目录下的模块和子包中的模块（ simple 和 advanced 下的命令模块）。
        """
        import importlib
        import pkgutil

        try:
            import CAD.commands as commands_pkg
        except Exception:
            return

        for finder, name, ispkg in pkgutil.iter_modules(commands_pkg.__path__):
            full_name = f"{commands_pkg.__name__}.{name}"
            try:
                if ispkg:
                    subpkg = importlib.import_module(full_name)
                    for sfinder, sname, sispkg in pkgutil.iter_modules(subpkg.__path__):
                        if sispkg:
                            continue
                        importlib.import_module(f"{full_name}.{sname}")
                else:
                    importlib.import_module(full_name)
            except Exception:
                continue


registry = CommandRegistry()
