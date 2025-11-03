from .base import Param, CommandMeta
from .registry import registry


def command(name: str, description: str = ""):
    """注册高级命令"""
    def decorator(cls):
        meta = getattr(cls, "_command_meta", None)
        if not meta:
            meta = CommandMeta(name=name, description=description, cls=cls)
        else:
            meta.name = name
            meta.description = description
            meta.cls = cls
        setattr(cls, "_command_meta", meta)
        registry.register_advanced(meta)
        return cls
    return decorator


def argument(short: str, long: str, type=str, required=False):
    """为命令类增加参数定义"""
    def decorator(cls):
        meta = getattr(cls, "_command_meta", None)
        if not meta:
            meta = CommandMeta(name="", description="", cls=cls)
            setattr(cls, "_command_meta", meta)
        meta.params.append(Param(short, long, type, required))
        return cls
    return decorator


def simple_command(name: str):
    """注册简单命令"""
    def decorator(func):
        registry.register_simple(name, func)
        return func
    return decorator
