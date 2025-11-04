import os
import json
import tomllib
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .loader import ConfigLoader

from mylib.etp import ConfigError


class FileLoader:
    """负责加载和解析 TOML / JSON 配置文件"""
    def __init__(self, parent: "ConfigLoader"):
        self.parent = parent

    def load(self, config_path: str) -> None:
        """根据文件后缀自动选择解析器"""
        if not os.path.exists(config_path):
            raise ConfigError(f"配置文件不存在: {config_path}")

        if config_path.endswith(".toml"):
            self._load_toml(config_path)
        elif config_path.endswith(".json"):
            self._load_json(config_path)
        else:
            raise ConfigError(f"未知的配置文件类型: {config_path}")

    def _load_toml(self, path: str) -> None:
        try:
            with open(path, "rb") as f:
                data = tomllib.load(f)
                self.parent.toml_data = data
                self.parent._record_source("toml_data", "config -> toml")

            fastapi = data.get("FastAPI_Server", {})
            if isinstance(fastapi, dict):
                self._register("fastapi_server_host", fastapi.get("fastapi_server_host"))
                self._register("fastapi_server_port", fastapi.get("fastapi_server_port"))

            napcat = data.get("Napcat_Server", {})
            if isinstance(napcat, dict):
                self._register("napcat_server_host", napcat.get("napcat_server_host"))
                self._register("napcat_server_port", napcat.get("napcat_server_port"))
                self._register("napcat_server_token", napcat.get("napcat_server_token"))

        except Exception as e:
            raise ConfigError(f"TOML 配置解析失败 ({path}): {e}")

    def _load_json(self, path: str) -> None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.parent.json_data = data
                self.parent._record_source("json_data", "config -> json")

            fastapi = data.get("FastAPI_Server", {})
            if isinstance(fastapi, dict):
                self._register("fastapi_server_host", fastapi.get("fastapi_server_host"))
                self._register("fastapi_server_port", fastapi.get("fastapi_server_port"))

            napcat = data.get("Napcat_Server", {})
            if isinstance(napcat, dict):
                self._register("napcat_server_host", napcat.get("napcat_server_host"))
                self._register("napcat_server_port", napcat.get("napcat_server_port"))
                self._register("napcat_server_token", napcat.get("napcat_server_token"))

        except Exception as e:
            raise ConfigError(f"JSON 配置解析失败 ({path}): {e}")

    def _register(self, name: str, value: Any) -> None:
        """通过父类接口注册属性"""
        if value is not None:
            self.parent._register_attribute(name, value, "config -> file_loader")
