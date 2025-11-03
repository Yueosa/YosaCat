# config_loader.py
import os
import json
import tomllib
import inspect
from dotenv import load_dotenv
from typing import Dict, Literal, Optional

from mylib.etp import ConfigError, EnvError
from mylib.utils import Printer


class ConfigLoader:
    """
    ConfigLoader 配置加载器 (支持全局单例模式) 

    支持：
    - TOML 配置 (推荐) 
    - JSON 兼容模式
    - .env 环境变量文件

    默认加载路径：
        ./mylib/config/config.toml
    """

    # ------------------- 全局单例模式喵~ -------------------
    _global_instance: Optional["ConfigLoader"] = None

    @classmethod
    def init_global(cls, mode: Literal["env", "config", "all"] = "config",
                    config_path: Optional[str] = None) -> "ConfigLoader":
        """初始化全局实例"""
        if cls._global_instance is None:
            cls._global_instance = cls(mode=mode, config_path=config_path)
        return cls._global_instance

    @classmethod
    def get_global(cls) -> "ConfigLoader":
        """获取全局实例"""
        if cls._global_instance is None:
            raise RuntimeError("ConfigLoader 未初始化，请先调用 init_global()")
        return cls._global_instance

    # ------------------- 实例化吧! -------------------
    def __init__(self,
                mode: Literal["env", "config", "all"] = "config",
                config_path: Optional[str] = None):
        self._source_map: Dict[str, str] = {}
        self.printer = Printer()

        if config_path is None:
            self.config_path = os.path.join(
                os.path.dirname(__file__), "config.toml"
            )
            self._record_source("config_path", "__init__ -> default (mylib/config/config.toml)")
        else:
            caller_frame = inspect.stack()[1]
            caller_file = os.path.abspath(caller_frame.filename)
            caller_dir = os.path.dirname(caller_file)

            if not os.path.isabs(config_path):
                resolved_path = os.path.abspath(os.path.join(caller_dir, config_path))
            else:
                resolved_path = config_path

            self.config_path = resolved_path
            self._record_source("config_path", "__init__ -> caller_relative_resolve")

        getattr(self, f"_load_{mode}")()

    # ------------------- 你只是个工具罢了... -------------------
    def _record_source(self, name: str, source: str) -> None:
        """记录属性来源"""
        self._source_map[name] = source

    # ------------------- 配置加载器 -------------------
    def _load_config(self) -> None:
        """优先加载 TOML 配置文件, 兼容 JSON 配置文件"""
        if not os.path.exists(self.config_path):
            raise ConfigError(f"配置文件不存在: {self.config_path}")

        if self.config_path.endswith(".toml"):
            try:
                with open(self.config_path, "rb") as f:
                    toml_data = tomllib.load(f)
                    self.toml_data = toml_data
                    self._record_source("toml_data", "_load_config")

                    self.fastapi = toml_data.get("FastAPI_Server", {})
                    self._record_source("fastapi", "_load_config -> FastAPI_Server")

                    self.napcat = toml_data.get("Napcat_Server", {})
                    self._record_source("napcat", "_load_config -> Napcat_Server")

            except Exception as e:
                raise ConfigError(f"TOML 配置解析失败: {e}")
        elif self.config_path.endswith(".json"):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    json_data = json.load(f)
                    self.json_data = json_data
                    self._record_source("json_data", "_load_config -> JSON")
            except Exception as e:
                raise ConfigError(f"JSON 配置解析失败: {e}")
        else:
            raise ConfigError(f"未知的配置文件类型: {self.config_path}")

    # ------------------- 环境变量加载器 -------------------
    def _load_env(self) -> None:
        """加载 .env 环境变量"""
        try:
            load_dotenv()
            self.url: str = os.getenv("URL")
            self._record_source("url", "_load_env -> .env:URL")

            self.header: Dict[str, str] = {
                "Content-Type": "application/json",
                "Authorization": os.getenv("TOKEN"),
            }
            self._record_source("header", "_load_env -> .env:TOKEN")

            if not self.url:
                raise EnvError("环境变量 URL 未设置")
            if not self.header["Authorization"]:
                raise EnvError("环境变量 TOKEN 未设置")

        except Exception as e:
            raise EnvError(f"环境变量加载失败: {e}")

    # ------------------- 所有配置全部启动启动启动! -------------------
    def _load_all(self) -> None:
        """同时加载配置 + 环境变量"""
        self._load_config()
        self._load_env()
        self._record_source("load_mode", "_load_all (config + env)")

    # ------------------- 超级无敌调试模块 -------------------
    def show_summary(self) -> None:
        """打印当前配置摘要"""
        self.printer.cprint("cyan", f"📄 配置文件路径: {self.config_path}")
        
        if hasattr(self, "fastapi"):
            self.printer.cprint("green", f"    🌐 FastAPI 服务器: {self.fastapi}")
        if hasattr(self, "napcat"):
            self.printer.cprint("green", f"    🤖 Napcat 服务器: {self.napcat}")
        if hasattr(self, "url"):
            self.printer.cprint("yellow", f"    🔗 环境变量 URL: {self.url}")
        if hasattr(self, "header"):
            self.printer.cprint("yellow", f"    🔑 认证 TOKEN: {self.header}")

        self.printer.cprint("magenta", "\n🧭 属性来源追踪:")
        for key, src in self._source_map.items():
            self.printer.cprint("blue", f"    - {key:<12} ← {src}")
