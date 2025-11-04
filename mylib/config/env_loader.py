import os
from dotenv import load_dotenv
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .loader import ConfigLoader

from mylib.etp import EnvError


class EnvLoader:
    """负责加载和校验 .env 环境变量"""

    REQUIRED_VARS = ["URL", "TOKEN"]

    def __init__(self, parent: "ConfigLoader"):
        self.parent = parent

    def load(self) -> None:
        """加载环境变量"""
        try:
            load_dotenv()

            url = os.getenv("URL")
            token = os.getenv("TOKEN")

            self._validate_required(url, token)

            self._register("url", url)
            self._register("header", {
                "Content-Type": "application/json",
                "Authorization": token,
            })

        except Exception as e:
            raise EnvError(f"环境变量加载失败: {e}")

    def _register(self, name: str, value):
        """注册属性并追踪来源"""
        self.parent._register_attribute(name, value, "config -> env")

    def _validate_required(self, url: str, token: str) -> None:
        """校验环境变量必需项"""
        missing = []
        if not url:
            missing.append("URL")
        if not token:
            missing.append("TOKEN")

        if missing:
            raise EnvError(f"缺少必要的环境变量: {', '.join(missing)}")
