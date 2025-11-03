import shlex
from .registry import registry


class CommandParser:
    def parse(self, text: str):
        text = text.strip()

        # 简单命令：/ping
        if text.startswith("/"):
            name = text.split()[0]
            if name in registry.simple_commands:
                return ("simple", name, {})
            raise ValueError(f"未知简单命令: {name}")

        # 高级命令：<msg> -o x -m y -df --set=123
        elif text.startswith("<") and ">" in text:
            name = text[1:text.index(">")]
            tokens = shlex.split(text[text.index(">") + 1:], posix=False)
            params = self._parse_params(tokens)
            return ("advanced", name, params)

        else:
            raise ValueError("无法识别的命令格式")

    def _parse_params(self, tokens):
        params = {}
        i = 0
        while i < len(tokens):
            token = tokens[i]

            # 1️⃣ 长参数赋值 --key=value
            if token.startswith("--") and "=" in token:
                key, value = token.split("=", 1)
                params[key] = value
                i += 1

            # 2️⃣ 长参数单独使用 --key value
            elif token.startswith("--"):
                # 注意：必须防止 "--o" 这种非法长参数通过
                if len(token) <= 3:
                    # "--" 或 "--o" 都视为非法长参数
                    print(f"⚠️  忽略非法长参数: {token}")
                    i += 1
                    continue
                if i + 1 < len(tokens) and not tokens[i + 1].startswith("-"):
                    params[token] = tokens[i + 1]
                    i += 2
                else:
                    params[token] = True
                    i += 1

            # 3️⃣ 短参数赋值 -k=value
            elif token.startswith("-") and "=" in token:
                key, value = token.split("=", 1)
                params[key] = value
                i += 1

            # 4️⃣ 多短参数连写 -abc → {'-a': True, '-b': True, '-c': True}
            elif token.startswith("-") and not token.startswith("--") and len(token) > 2 and "=" not in token:
                for ch in token[1:]:
                    params[f"-{ch}"] = True
                i += 1

            # 5️⃣ 单短参数 -o 123 或 -f
            elif token.startswith("-") and not token.startswith("--"):
                if i + 1 < len(tokens) and not tokens[i + 1].startswith("-"):
                    params[token] = tokens[i + 1]
                    i += 2
                else:
                    params[token] = True
                    i += 1

            # 6️⃣ 其他内容（忽略）
            else:
                i += 1

        return params

import sys, os
sys.path.append(os.path.dirname(__file__))

from CAD import CommandParser, registry

def execute_command(text: str):
    parser = CommandParser()
    cmd_type, name, params = parser.parse(text)
    print(cmd_type, name, params)

    if cmd_type == "simple":
        registry.simple_commands[name]()
    elif cmd_type == "advanced":
        meta = registry.get_advanced(name)
        if not meta:
            print(f"未知高级命令 <{name}>")
            return
        if hasattr(meta, "cls"):
            cls = meta.cls
        else:
            cls = meta["cls"]
        cmd = cls(params)
        cmd.execute()
    return name, params


if __name__ == "__main__":
    execute_command("/ping")
    execute_command("<msg> -o 123456 -m ”hello 小恋“")
