from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .loader import ConfigLoader

from mylib.utils import Printer


class Summary:
    """统一管理 ConfigLoader 的调试与打印"""
    def __init__(self, parent: "ConfigLoader"):
        self.parent = parent
        self.printer = Printer()

    def show_required(self) -> None:
        """打印运行必备字段及状态"""
        cfg = self.parent
        p = self.printer

        p.cprint("cyan", f"📄 配置文件路径: {cfg.config_path}")

        if hasattr(cfg, "fastapi_server_host"):
            p.cprint("green", f"    🌐 FastAPI Host: {cfg.fastapi_server_host}")
        if hasattr(cfg, "fastapi_server_port"):
            p.cprint("green", f"    🌐 FastAPI Port: {cfg.fastapi_server_port}")

        if hasattr(cfg, "napcat_server_host"):
            p.cprint("green", f"    🤖 Napcat Host: {cfg.napcat_server_host}")
        if hasattr(cfg, "napcat_server_port"):
            p.cprint("green", f"    🤖 Napcat Port: {cfg.napcat_server_port}")
        if hasattr(cfg, "napcat_server_token"):
            p.cprint("green", f"    🤖 Napcat Token: {cfg.napcat_server_token[:6]}...")

        if hasattr(cfg, "url"):
            p.cprint("yellow", f"    🔗 URL: {cfg.url}")
        if hasattr(cfg, "header"):
            p.cprint("yellow", f"    🔑 TOKEN: {cfg.header.get('Authorization', '未设置')}")

        p.cprint("magenta", "\n🔐 必须配置项状态:")
        missing = []
        for key in cfg.CONFIG:
            if hasattr(cfg, key):
                val = getattr(cfg, key)
                p.cprint("green", f"    ✅ {key}: {val}")
            else:
                missing.append(key)
                p.cprint("red", f"    ❌ {key}: 未设置")

        if missing:
            p.cprint("red", f"\n🚨 缺少关键配置: {', '.join(missing)}")

        p.cprint("magenta", "\n🧭 属性来源追踪:")
        for k, src in cfg.tracker.map.items():
            p.cprint("blue", f"    - {k:<24} ← {src}")

    def show_discovery(self) -> None:
        """打印自动发现的配置节与来源"""
        cfg = self.parent
        p = self.printer

        p.cprint("cyan", f"\n🧭 自动发现配置摘要 ({cfg.config_path}):\n")

        discovered = getattr(cfg, "discovery", None)
        if discovered is not None and discovered.discovered:
            p.cprint("magenta", f"📘 共发现 {len(discovered.discovered)} 个配置节:")
            for name, section in discovered.discovered.items():
                p.cprint("green", f"  - {name}")
                for k, v in section.items():
                    p.cprint("blue", f"      {k}: {v}")
        else:
            if self.parent._mode == "discovery":
                p.cprint("yellow", "（未发现任何自动配置节）")

        if discovered:
            p.cprint("red", f"\n🚫 黑名单节: {', '.join(discovered.blacklist)}")

        if cfg.tracker.discovered_attrs:
            p.cprint("magenta", "\n📍 发现属性追踪:")
            for name in cfg.tracker.discovered_attrs:
                src = cfg.tracker.map.get(name, "unknown")
                p.cprint("blue", f"    - {name:<24} ← {src}")
