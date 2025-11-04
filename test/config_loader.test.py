import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from mylib import ConfigLoader

from mylib import Printer


if __name__ == "__main__":
    print("\n\n=== 测试 1: 默认加载 mylib/config/config.toml ===")
    try:
        cfg = ConfigLoader(mode="config")
        cfg.show_config()
        print("✅ 测试 1 成功\n")
    except Exception as e:
        print(f"❌ 测试 1 失败: {e}")

    print("\n\n=== 测试 2: 同时加载 config + env ===")
    try:
        cfg2 = ConfigLoader(mode="config")
        cfg2._load_env()
        cfg2.show_config()
        print("✅ 测试 2 成功\n")
    except Exception as e:
        print(f"❌ 测试 2 失败: {e}")

    print("\n\n=== 测试 3: 根目录加载 ../config.toml ===")
    try:
        cfg3 = ConfigLoader(mode="config", config_path="../config.toml")
        cfg3.show_config()
        print("✅ 测试 3 成功\n")
    except Exception as e:
        print(f"❌ 测试 3 失败: {e}")

    print("\n\n=== 测试 4: 根目录加载 ../config.json ===")
    try:
        cfg4 = ConfigLoader(mode="config", config_path="../config.json")
        cfg4.show_config()
        print("✅ 测试 4 成功\n")
    except Exception as e:
        print(f"❌ 测试 4 失败: {e}")

    print("\n\n=== 测试 5: 自动发现模式 ===")
    try:
        cfg5 = ConfigLoader(mode="discovery", config_path="../config.example.toml")
        cfg5.show_config()

        print("\n=== 基础属性访问测试 ===")
        Printer().cprint("cyan", f"cfg5.Lian_Love: {cfg5.Lian_Love}")  # ConfigDictWrapper
        Printer().cprint("cyan", f"cfg5.Lian_Love.Test.test: {cfg5.Lian_Love.Test.test}")  # "你好"
        Printer().cprint("cyan", f"cfg5.Lian_Love.message: {cfg5.Lian_Love.message}")  # "小恋最喜欢你了哦"
        Printer().cprint("cyan", f"cfg5.Lian_Love.age: {cfg5.Lian_Love.age}")  # 17
        Printer().cprint("cyan", f"cfg5.Lian_Love.bool: {cfg5.Lian_Love.bool}")  # True

        print("\n=== 列表和嵌套访问测试 ===")
        Printer().cprint("cyan", f"cfg5.Lian_Love.List.item[0].name: {cfg5.Lian_Love.List.item[0].name}")  # "A"
        Printer().cprint("cyan", f"cfg5.Lian_Love.List.item[1].name: {cfg5.Lian_Love.List.item[1].name}")  # "B"
        Printer().cprint("cyan", f"cfg5.Lian_Love.List.item 长度: {len(cfg5.Lian_Love.List.item)}")  # 2

        print("\n=== 原始数据访问测试 (.raw) ===")
        Printer().cprint("cyan", f"cfg5.Lian_Love.raw: {cfg5.Lian_Love.raw}")  # 完整字典
        Printer().cprint("cyan", f"cfg5.Lian_Love.List.item.raw: {cfg5.Lian_Love.List.item.raw}")  # 列表原始数据
        Printer().cprint("cyan", f"cfg5.Lian_Love.Test.raw: {cfg5.Lian_Love.Test.raw}")  # Test节原始数据

        print("\n=== 下划线方法调用测试 ===")
        print("1. _items() 方法:")
        print("   Lian_Love._items():")
        for key, value in cfg5.Lian_Love._items():
            Printer().cprint("cyan", f"     {key}: {value}")

        print("\n2. _get() 方法:")
        Printer().cprint("cyan", f"   Lian_Love._get('message'): {cfg5.Lian_Love._get('message')}")
        Printer().cprint("cyan", f"   Lian_Love._get('nonexistent', '默认值'): {cfg5.Lian_Love._get('nonexistent', '默认值')}")

        print("\n3. _keys() 方法:")
        Printer().cprint("cyan", f"   Lian_Love._keys(): {list(cfg5.Lian_Love._keys())}")

        print("\n4. _values() 方法:")
        print("   Lian_Love._values():")
        for value in cfg5.Lian_Love._values():
            Printer().cprint("cyan", f"     {value}")

        print("\n5. _dict() 方法:")
        Printer().cprint("cyan", f"   Lian_Love._dict(): {cfg5.Lian_Love._dict()}")

        print("\n=== 嵌套结构方法测试 ===")
        print("Lian_Love.Test._items():")
        for key, value in cfg5.Lian_Love.Test._items():
            Printer().cprint("cyan", f"  {key}: {value}")

        print("Lian_Love.List._items():")
        for key, value in cfg5.Lian_Love.List._items():
            Printer().cprint("cyan", f"  {key}: {value}")

        print("\n=== 列表迭代测试 ===")
        print("遍历 Lian_Love.List.item:")
        for i, item in enumerate(cfg5.Lian_Love.List.item):
            Printer().cprint("cyan", f"  第{i}项: {item.name} (原始数据: {item.raw})")

        print("\n=== 错误处理测试 ===")
        try:
            print(cfg5.Lian_Love.nonexistent)
        except AttributeError as e:
            print(f"✅ 访问不存在的属性正确抛出异常: {e}")

        try:
            print(cfg5.Lian_Love.List.item[999])
        except (KeyError, IndexError) as e:
            print(f"✅ 访问越界索引正确抛出异常: {e}")

        print("\n=== 类型检查测试 ===")
        Printer().cprint("cyan", f"Lian_Love 类型: {type(cfg5.Lian_Love)}")
        Printer().cprint("cyan", f"Lian_Love.List.item 类型: {type(cfg5.Lian_Love.List.item)}")
        Printer().cprint("cyan", f"Lian_Love.List.item[0] 类型: {type(cfg5.Lian_Love.List.item[0])}")
        Printer().cprint("cyan", f"Lian_Love.message 类型: {type(cfg5.Lian_Love.message)}")

        print("\n=== 综合使用示例 ===")
        # 模拟实际使用场景
        print("配置信息汇总:")
        Printer().cprint("cyan", f"- 消息: {cfg5.Lian_Love.message}")
        Printer().cprint("cyan", f"- 年龄: {cfg5.Lian_Love.age}")
        Printer().cprint("cyan", f"- 测试信息: {cfg5.Lian_Love.Test.test}")
        print(f"- 列表项:")
        for item in cfg5.Lian_Love.List.item:
            Printer().cprint("cyan", f"  * {item.name}")

        print("✅ 测试 5 成功 - 所有功能正常！\n")
    except Exception as e:
        print(f"❌ 测试 5 失败: {e}")

    print("\n\n✅ 所有测试执行完毕")

