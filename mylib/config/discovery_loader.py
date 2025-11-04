from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from .loader import ConfigLoader

from .base import ConfigDictWrapper


class DiscoveryLoader:
    """负责从 TOML/JSON 数据中自动发现并注册非黑名单配置节"""
    def __init__(self, parent: "ConfigLoader"):
        self.parent = parent
        self.blacklist = ["FastAPI_Server", "Napcat_Server"]
        self.discovered: Dict[str, Dict[str, Any]] = {}

    def discover(self) -> None:
        """自动发现配置节"""
        try:
            toml_data = object.__getattribute__(self.parent, "toml_data")
        except AttributeError:
            toml_data = None
            
        try:
            json_data = object.__getattribute__(self.parent, "json_data")
        except AttributeError:
            json_data = None

        if isinstance(toml_data, dict):
            self._discover_mapping(toml_data, "discovery -> toml")

        if isinstance(json_data, dict):
            self._discover_mapping(json_data, "discovery -> json")

    def _discover_mapping(self, data: dict, source_tag: str) -> None:
        for section_name, section_data in data.items():
            if section_name in self.blacklist:
                self.parent._record_source(f"skip_{section_name}", f"{source_tag} (blacklisted)")
                continue

            if isinstance(section_data, dict):
                wrapper = ConfigDictWrapper(section_data, f"{source_tag}.{section_name}")
                self._register(section_name, wrapper, source_tag)
                self.discovered[section_name] = section_data
            else:
                self.parent._record_source(f"skip_{section_name}", f"{source_tag} (non-dict)")

    def _register(self, name: str, value: Any, source: str) -> None:
        """通过父类接口注册属性"""
        self.parent._register_attribute(name, value, source)
