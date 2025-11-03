# config_loader.py
import os
import json
import tomllib
import inspect
from dotenv import load_dotenv
from typing import Dict, Literal, Optional, List, Any

from mylib.etp import ConfigError, EnvError
from mylib.utils import Printer


class ConfigLoader:
    """
    ConfigLoader 配置加载器 (支持全局单例模式) 

    支持：
    - TOML 配置 (推荐) 
    - JSON 兼容模式
    - .env 环境变量文件
    - 自动发现模式

    默认加载路径：
        ./mylib/config/config.toml
    """

    # ------------------- 必须配置项列表 -------------------
    REQUIRED_CONFIGS = [
        "fastapi_host",
        "fastapi_port", 
        "napcat_url",
        "database_url"
    ]

    # ------------------- 实例化 -------------------
    def __init__(self,
                mode: Literal["env", "config", "all", "discovery"] = "config",
                config_path: Optional[str] = None):
        self._source_map: Dict[str, str] = {}
        self._discovered_attrs: List[str] = []  # 记录自动发现的属性
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

        # 验证必须配置项
        self._validate_required_configs()



    # ------------------- 工具方法 -------------------


    # ------------------- 配置加载器 -------------------

    def _load_json_config(self) -> None:
        """加载 JSON 配置"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                self.json_data = json_data
                self._record_source("json_data", "_load_config -> JSON")
        except Exception as e:
            raise ConfigError(f"JSON 配置解析失败: {e}")

    # ------------------- 环境变量加载器 -------------------


    # ------------------- 自动发现模式 -------------------
    def _load_discovery(self) -> None:
        """自动发现模式：加载所有配置并自动注册属性"""
        self._load_config()
        self._load_env()
        self._discover_from_toml()
        self._discover_from_json() 
        self._discover_from_env()
        self._record_source("load_mode", "_load_discovery (config + env + auto_discovery)")

    def _discover_from_toml(self) -> None:
        """从 TOML 数据中发现配置"""
        if hasattr(self, 'toml_data'):
            for section_name, section_data in self.toml_data.items():
                if isinstance(section_data, dict):
                    for key, value in section_data.items():
                        attr_name = f"{section_name}_{key}"
                        self._register_attribute(attr_name, value, "discovery -> toml")

    def _discover_from_json(self) -> None:
        """从 JSON 数据中发现配置"""
        if hasattr(self, 'json_data'):
            if isinstance(self.json_data, dict):
                for key, value in self.json_data.items():
                    self._register_attribute(key, value, "discovery -> json")

    def _discover_from_env(self) -> None:
        """从环境变量中发现配置"""
        # 获取所有环境变量（除了常见的系统变量）
        common_system_vars = {'PATH', 'HOME', 'USER', 'LANG', 'PYTHONPATH'}
        for key, value in os.environ.items():
            if key not in common_system_vars and value.strip():
                self._register_attribute(key, value, "discovery -> env")

    # ------------------- 所有配置全部加载 -------------------
    def _load_all(self) -> None:
        """同时加载配置 + 环境变量"""
        self._load_config()
        self._load_env()
        self._record_source("load_mode", "_load_all (config + env)")

    # ------------------- 属性检查和方法 -------------------
    def get_all_attributes(self) -> Dict[str, Any]:
        """获取所有实例属性（排除私有方法）"""
        attrs = {}
        for key in dir(self):
            if not key.startswith('_') and not callable(getattr(self, key)):
                attrs[key] = getattr(self, key)
        return attrs

    def get_attribute_sources(self) -> Dict[str, str]:
        """获取所有属性的来源"""
        return self._source_map.copy()

    # ------------------- 增强的调试模块 -------------------
    def show_summary(self) -> None:
        """打印当前配置摘要"""
        self.printer.cprint("cyan", f"📄 配置文件路径: {self.config_path}")
        
        # 打印核心配置
        if hasattr(self, "fastapi"):
            self.printer.cprint("green", f"    🌐 FastAPI 服务器: {self.fastapi}")
        if hasattr(self, "napcat"):
            self.printer.cprint("green", f"    🤖 Napcat 服务器: {self.napcat}")
        if hasattr(self, "url"):
            self.printer.cprint("yellow", f"    🔗 环境变量 URL: {self.url}")
        if hasattr(self, "header"):
            self.printer.cprint("yellow", f"    🔑 认证 TOKEN: {self.header.get('Authorization', '未设置')}")

        # 打印所有发现的属性
        all_attrs = self.get_all_attributes()
        if all_attrs:
            self.printer.cprint("magenta", "\n📋 所有配置属性:")
            for key, value in all_attrs.items():
                if key not in ['fastapi', 'napcat', 'url', 'header', 'toml_data', 'json_data']:
                    source = self._source_map.get(key, "unknown")
                    self.printer.cprint("blue", f"    - {key}: {value} ← {source}")

        # 打印必须配置项状态
        self.printer.cprint("red", "\n🔐 必须配置项状态:")
        for config_name in self.REQUIRED_CONFIGS:
            status = "✅ 已设置" if hasattr(self, config_name) else "❌ 缺失"
            value = getattr(self, config_name, "未设置")
            self.printer.cprint("red" if status == "❌ 缺失" else "green", 
                                f"    - {config_name}: {value} ({status})")

        self.printer.cprint("magenta", "\n🧭 属性来源追踪:")
        for key, src in self._source_map.items():
            if key in ['fastapi', 'napcat', 'url', 'header'] or key in self._discovered_attrs:
                self.printer.cprint("blue", f"    - {key:<20} ← {src}")

    def show_required_configs(self) -> None:
        """专门显示必须配置项状态"""
        self.printer.cprint("cyan", "🔐 必须配置项检查:")
        for config_name in self.REQUIRED_CONFIGS:
            if hasattr(self, config_name):
                value = getattr(self, config_name)
                self.printer.cprint("green", f"    ✅ {config_name}: {value}")
            else:
                self.printer.cprint("red", f"    ❌ {config_name}: 未设置")

"""
# 使用自动发现模式
cfg = ConfigLoader(mode="discovery", config_path="./config.toml")

# 访问必须配置项（会自动检查）
print(cfg.fastapi_host)  # 如果未设置会抛出 ConfigError

# 访问自动发现的配置项
print(cfg.fastapi_server_host)  # 自动从 [FastAPI_Server] host 发现
print(cfg.database_url)         # 自动发现

# 查看所有属性
cfg.show_summary()

# 专门检查必须配置项
cfg.show_required_configs()
"""
