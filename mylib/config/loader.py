# config_loader.py
import os
import inspect
from typing import Literal, Optional, Any

from .base import ConfigDictWrapper
from .summary import Summary
from .source_tracker import SourceTracker
from .discovery_loader import DiscoveryLoader
from .env_loader import EnvLoader
from .file_loader import FileLoader

from mylib.etp import ConfigError


class ConfigLoader:
    """
    ConfigLoader 配置加载器 (支持全局单例模式) 

    支持：
    - TOML 配置 (推荐) (兼容JSON)
    - .env 环境变量文件
    - config 自动发现模式

    默认加载路径：
        ./mylib/config/config.toml
    """

    CONFIG = [
        "fastapi_server_host",
        "fastapi_server_port",
        "napcat_server_host",
        "napcat_server_port",
        "napcat_server_token"
    ]

    def __setattr__(self, name: str, value: Any) -> None:
        """记录属性设置来源"""
        super().__setattr__(name, value)
        if not name.startswith('_') and hasattr(self, "tracker"):
            if name not in self.tracker.map:
                caller_frame = inspect.stack()[1]
                caller_func = caller_frame.function
                self._record_source(name, f"{self.__class__.__name__} -> {caller_func}")

    def __getattr__(self, name: str) -> Any:
        """
        动态解析配置数据
        支持嵌套的字典和列表访问
        """
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            pass
        
        if self._mode != "discovery":
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        
        try:
            toml_data = object.__getattribute__(self, "toml_data")
        except AttributeError:
            toml_data = None
            
        try:
            json_data = object.__getattribute__(self, "json_data")
        except AttributeError:
            json_data = None
        
        if isinstance(toml_data, dict) and name in toml_data:
            data = toml_data[name]
            return ConfigDictWrapper(data, f"toml.{name}")
        
        if isinstance(json_data, dict) and name in json_data:
            data = json_data[name]
            return ConfigDictWrapper(data, f"json.{name}")
        
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


    # ------------------- 实例化吧! -------------------
    def __init__(self,
                mode: Literal["env", "config", "discovery"] = "discovery",
                config_path: Optional[str] = None):
        self.tracker = SourceTracker()
        self.summary = Summary(self)
        self._mode = mode

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

        self._validate_required_configs()


    # ------------------- 全局单例模式喵~ -------------------
    _global_instance: Optional["ConfigLoader"] = None

    @classmethod
    def init_global(cls, mode: Literal["env", "config", "discovery"] = "discovery",
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


    # ------------------- 验证运行必备字段喵 -------------------
    def _validate_required_configs(self) -> None:
        """验证必须配置项"""
        missing_configs = []
        for config_name in self.CONFIG:
            if not hasattr(self, config_name):
                missing_configs.append(config_name)
        
        if missing_configs:
            raise ConfigError(f"缺少必须配置项: {missing_configs}")


    # ------------------- 实例属性注册喵 -------------------
    def _register_attribute(self, name: str, value: Any, source: str) -> None:
        """注册实例属性"""
        setattr(self, name, value)
        self._record_source(name, source)

    def _record_source(self, name: str, source: str) -> None:
        self.tracker.record(name, source)


    # ------------------- 核心业务: 配置加载函数喵 -------------------
    def _load_config(self) -> None:
        """加载配置文件 (统一入口)"""
        self.file_loader = FileLoader(self)
        self.file_loader.load(self.config_path)

    def _load_env(self) -> None:
        """加载环境变量 (.env)"""
        self.env_loader = EnvLoader(self)
        self.env_loader.load()

    def _load_discovery(self) -> None:
        self._load_config()
        self.discovery = DiscoveryLoader(self)
        self.discovery.discover()


    # ------------------- 可视化打印配置信息喵 -------------------
    def show_config(self) -> None:
        self.summary.show_required()
        self.summary.show_discovery()
