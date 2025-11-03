import sys, os
sys.path.append(os.path.dirname(__file__))

from ETP import *

import json
from dotenv import load_dotenv
from typing import List, Dict, Literal


class ConfigLoader:
    def __init__(
            self,
            mode: Literal["env", "config", "all"] = "all"
    ):
        if mode == "all":
            self._load_all()

        if mode == "config":
            self._load_config()
        
        if mode == "env":
            self._load_env()
    
    def _load_config(self, path: str = "app.config.json") -> int:
        try:
            with open(path, 'r', encoding="utf-8") as f:
                json_data = json.load(f)
                self.group: List[int] = json_data["group"]
                self.message_list: List[str] = json_data["message_type"]["message"]
                self.image_list: List[str] = json_data["message_type"]["image"]
                self.test_list: List[str] = json_data["message_type"]["test"]
        except FileNotFoundError:
            raise ConfigError(f"配置文件不存在: {path}")
        except (json.JSONDecodeError, KeyError) as e:
            raise ConfigError(f"配置文件格式错误: {e}")

        if self.group and self.message_list and self.image_list and self.test_list:
            return 1
        else:
            raise ConfigError("配置文件字段不完整或为空")
    
    def _load_env(self) -> int:
        try:
            load_dotenv()
            self.url: str = os.getenv("URL")
            self.header: Dict[str, str] = {
                "Content-Type": "application/json",
                "Authorization": os.getenv("TOKEN")
            }

            if not self.url:
                raise EnvError("环境变量 URL 未设置")
            if not self.header["Authorization"]:
                raise EnvError("环境变量 HEADER_AUTH 未设置")

        except Exception as e:
            raise EnvError(f"环境变量加载失败: {e}")

        return 1
    
    def _load_all(self) -> int:
        self._load_config()
        self._load_env()
