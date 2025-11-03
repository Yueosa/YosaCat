import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from mylib import ConfigLoader

if __name__ == "__main__":
    print("\n\n=== 测试 1: 默认加载 mylib/config/config.toml ===")
    cfg = ConfigLoader(mode="config")
    cfg.show_summary()

    print("\n\n=== 测试 2: 同时加载 config + env ===")
    cfg2 = ConfigLoader(mode="all")
    cfg2.show_summary()

    print("\n\n=== 测试 3: 根目录加载 /config.toml ===")
    cfg3 = ConfigLoader(mode="config", config_path="../config.toml")
    cfg3.show_summary()

    print("\n\n=== 测试 4: 根目录同时加载 config + env ===")
    cfg4 = ConfigLoader(mode="all", config_path="../config.toml")
    cfg4.show_summary()

    print("\n\n✅ 所有测试执行完毕")
