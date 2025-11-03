from dataclasses import dataclass, field
from typing import List, Type, Any


@dataclass
class Param:
    """表示一个命令参数/选项的定义。
    short: 短形式 (例如 '-o' ) 
    long: 长形式 (例如 '--object' ) 
    value_type: 期望的值类型 (用于转换，当前实现不自动转换 ) 
    required: 是否为必填参数
    """
    short: str
    long: str
    value_type: type = str
    required: bool = False


@dataclass
class CommandMeta:
    """高级命令的元数据 (描述 ) 。
    name: 命令名 (如 'msg' ) 
    description: 命令说明
    params: 参数定义列表 (Param ) 
    cls: 对应的命令实现类 (子类继承自 BaseCommand ) 
    """
    name: str
    description: str
    params: List[Param] = field(default_factory=list)
    cls: Type = None


class BaseCommand:
    """高级命令实现的基类。
    构造时接收解析后的 params (dict)，提供 get(*names, default=None) 按多个别名查找参数值并根据 CommandMeta.Param.value_type 自动转换。
    """
    def __init__(self, params):
        self.params = params

    def _find_param_meta(self, name: str) -> Param | None:
        """根据短/长名在类上绑定的 _command_meta 中查找 Param 元数据。"""
        meta = getattr(self.__class__, "_command_meta", None)
        if not meta:
            return None
        for p in meta.params:
            if p.short == name or p.long == name:
                return p
        return None

    def _convert_value(self, raw: Any, target_type: Any) -> Any:
        """尝试将 raw 转换为 target_type。若失败则返回 raw。"""
        try:
            if target_type is bool:
                if raw is True or raw is False:
                    return bool(raw)
                if isinstance(raw, str):
                    r = raw.strip().lower()
                    if r in ("1", "true", "yes", "on"):
                        return True
                    if r in ("0", "false", "no", "off"):
                        return False
                    return True
                return bool(raw)

            if target_type is list:
                if isinstance(raw, list):
                    return raw
                if isinstance(raw, str):
                    return [s.strip() for s in raw.split(",") if s.strip() != ""]
                return [raw]

            if target_type is int:
                return int(raw)
            if target_type is float:
                return float(raw)

            if callable(target_type):
                return target_type(raw)

            return raw
        except Exception:
            return raw

    def get(self, *names, default=None):
        """按别名依次查找参数值；若找到并有对应 Param 定义，则做类型转换后返回。"""
        for n in names:
            if n in self.params:
                raw = self.params[n]
                param_meta = self._find_param_meta(n)
                if param_meta:
                    return self._convert_value(raw, param_meta.value_type)
                return raw
        return default
