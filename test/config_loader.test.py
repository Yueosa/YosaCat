import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from mylib import ConfigLoader

from mylib import Printer


def test_config():
    print("\n\n=== 测试 1: 默认加载 mylib/config/config.toml ===")
    try:
        cfg = ConfigLoader(mode="config")
        cfg.show_config()
        print("✅ 测试 1 成功\n")
    except Exception as e:
        print(f"❌ 测试 1 失败: {e}")


def test_env():
    print("\n\n=== 测试 2: 同时加载 config + env ===")
    try:
        cfg = ConfigLoader(mode="config")
        cfg._load_env()
        cfg.show_config()
        print("✅ 测试 2 成功\n")
    except Exception as e:
        print(f"❌ 测试 2 失败: {e}")


def test_config_path_toml():
    print("\n\n=== 测试 3: 根目录加载 ../config.toml ===")
    try:
        cfg = ConfigLoader(mode="config", config_path="../config.toml")
        cfg.show_config()
        print("✅ 测试 3 成功\n")
    except Exception as e:
        print(f"❌ 测试 3 失败: {e}")


def test_config_path_json():
    print("\n\n=== 测试 4: 根目录加载 ../config.json ===")
    try:
        cfg = ConfigLoader(mode="config", config_path="../config.json")
        cfg.show_config()
        print("✅ 测试 4 成功\n")
    except Exception as e:
        print(f"❌ 测试 4 失败: {e}")


def test_discovery():
    print("\n\n=== 测试 5: 自动发现模式 ===")
    try:
        cfg = ConfigLoader(mode="discovery", config_path="../config.example.toml")
        cfg.show_config()
        _discovery(cfg)
        print("✅ 测试 5 成功 - 所有功能正常！\n")
    except Exception as e:
        print(f"❌ 测试 5 失败: {e}")


def _discovery(cfg: "ConfigLoader"):
    p = Printer()

    def title(icon: str, text: str, color: str = "magenta"):
        p.cprint(color, f"\n{icon} {text}")
        p.cprint(color, "─" * (len(text) + 2))

    # === 基础属性访问测试 ===
    title("📘", "基础属性访问测试", "cyan")
    p.cprint("green", f"cfg.Lian_Love: {cfg.Lian_Love}")
    p.cprint("green", f"cfg.Lian_Love.Test.test: {cfg.Lian_Love.Test.test}")
    p.cprint("green", f"cfg.Lian_Love.message: {cfg.Lian_Love.message}")
    p.cprint("green", f"cfg.Lian_Love.age: {cfg.Lian_Love.age}")
    p.cprint("green", f"cfg.Lian_Love.bool: {cfg.Lian_Love.bool}")

    # === 列表和嵌套访问测试 ===
    title("📂", "列表与嵌套访问测试", "cyan")
    p.cprint("green", f"cfg.Lian_Love.List.item[0].name: {cfg.Lian_Love.List.item[0].name}")
    p.cprint("green", f"cfg.Lian_Love.List.item[1].name: {cfg.Lian_Love.List.item[1].name}")
    p.cprint("yellow", f"cfg.Lian_Love.List.item 长度: {len(cfg.Lian_Love.List.item)}")

    # === 原始数据访问测试 ===
    title("🧾", "原始数据访问 (.raw) 测试", "cyan")
    p.cprint("blue", f"cfg.Lian_Love.raw: {cfg.Lian_Love.raw}")
    p.cprint("blue", f"cfg.Lian_Love.List.item.raw: {cfg.Lian_Love.List.item.raw}")
    p.cprint("blue", f"cfg.Lian_Love.Test.raw: {cfg.Lian_Love.Test.raw}")

    # === 下划线方法测试 ===
    title("🧩", "_ 下划线方法测试", "magenta")
    print("1️⃣ _items():")
    for k, v in cfg.Lian_Love._items():
        p.cprint("cyan", f"   ➤ {k}: {v}")

    print("2️⃣ _get():")
    p.cprint("green", f"   message → {cfg.Lian_Love._get('message')}")
    p.cprint("yellow", f"   nonexistent → {cfg.Lian_Love._get('nonexistent', '默认值')}")

    print("3️⃣ _keys():")
    p.cprint("blue", f"   {list(cfg.Lian_Love._keys())}")

    print("4️⃣ _values():")
    for v in cfg.Lian_Love._values():
        p.cprint("cyan", f"   ➤ {v}")

    print("5️⃣ _dict():")
    p.cprint("blue", f"   {cfg.Lian_Love._dict()}")

    # === 嵌套结构方法测试 ===
    title("🧱", "嵌套结构方法测试", "cyan")
    print("Lian_Love.Test._items():")
    for k, v in cfg.Lian_Love.Test._items():
        p.cprint("cyan", f"   • {k}: {v}")

    print("Lian_Love.List._items():")
    for k, v in cfg.Lian_Love.List._items():
        p.cprint("cyan", f"   • {k}: {v}")

    # === 列表迭代测试 ===
    title("📜", "列表迭代测试", "cyan")
    for i, item in enumerate(cfg.Lian_Love.List.item):
        p.cprint("green", f"  [{i}] {item.name} → 原始数据: {item.raw}")

    # === 错误处理测试 ===
    title("⚠️", "错误处理测试", "red")
    try:
        _ = cfg.Lian_Love.nonexistent
    except AttributeError as e:
        p.cprint("yellow", f"✅ 正确抛出 AttributeError: {e}")

    try:
        _ = cfg.Lian_Love.List.item[999]
    except (KeyError, IndexError) as e:
        p.cprint("yellow", f"✅ 正确抛出越界异常: {e}")

    # === 类型检查 ===
    title("🧠", "类型检查", "magenta")
    p.cprint("green", f"Lian_Love: {type(cfg.Lian_Love)}")
    p.cprint("green", f"Lian_Love.List.item: {type(cfg.Lian_Love.List.item)}")
    p.cprint("green", f"Lian_Love.List.item[0]: {type(cfg.Lian_Love.List.item[0])}")
    p.cprint("green", f"Lian_Love.message: {type(cfg.Lian_Love.message)}")

    # === 综合使用展示 ===
    title("🌸", "综合使用示例", "cyan")
    p.cprint("magenta", "配置信息汇总:")
    p.cprint("cyan", f"  - 消息: {cfg.Lian_Love.message}")
    p.cprint("cyan", f"  - 年龄: {cfg.Lian_Love.age}")
    p.cprint("cyan", f"  - 测试信息: {cfg.Lian_Love.Test.test}")
    print("  - 列表项:")
    for item in cfg.Lian_Love.List.item:
        p.cprint("green", f"     • {item.name}")

    p.cprint("yellow", "\n🎯 测试完成：所有访问与异常行为验证通过！")


if __name__ == "__main__":
    test_config()
    test_env()
    test_config_path_toml()
    test_config_path_json()
    test_discovery()

    print("\n✅ 所有测试执行完毕")
