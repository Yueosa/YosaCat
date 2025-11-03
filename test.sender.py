import json
from requests import post
from typing import Literal

from message_builder import build_group_message
from config_loader import ConfigLoader


class MessageSender:
    def __init__(self):
        self.cfg = ConfigLoader()

    def _send_request_with_retry(\
            self,
            url: str,
            data: str,
            header: dict,
    ) -> None:
        response = post(url, data=data, headers=header)
        print(response)

    def send_message(
            self,
            mode: Literal["msg", "img", "api"]
    ) -> None:
        if mode == "msg":
            self.send_group_msg()

    def send_group_img(self, group_id: int):
        with open('test_image', 'r', encoding='utf-8') as f:
            img = f.read()

        msg: dict = {
            "group_id": group_id,
            "message": [{
                "type": "image",
                "data": {
                    "file": img
                }
            }
            ]
        }

        send_msg = json.dumps(msg)
        url: str = self.cfg.url + "/send_group_msg"
        self._send_request_with_retry(url, send_msg, self.cfg.header)

    def send_group_img_loli(self, group_id: int):
        send_msg = build_group_message(group_id, "image", image_file_data="https://www.loliapi.com/bg/")
        url: str = self.cfg.url + "/send_group_msg"
        self._send_request_with_retry(url, send_msg, self.cfg.header)

    def send_group_msg(
            self,
            group_id: int,
            msg: str = "miss you~"
    ) -> None:
        send_msg = build_group_message(group_id, "text", text_data=msg)
        url: str = self.cfg.url + "/send_group_msg"
        print(send_msg, "\n", url)
        self._send_request_with_retry(url, send_msg, self.cfg.header)

    def send_msg(
            self,
            id: int,
            msg: str = ""
    ) -> None:
        send_msg = build_group_message(id, "text", text_data=msg)
        url: str = self.cfg.url + "/send_group_msg"
        print(send_msg, "\n", url)
        self._send_request_with_retry(url, send_msg, self.cfg.header)

    def send_msg_test(
            self,
            id: int,
            msg: str = ""
    ) -> None:
        """
        本地转义 Unicode 形式发送消息，用于 Napcat 不支持 UTF-8 的情况。
        """
        # --- 先构造消息 ---
        send_msg = build_group_message(id, "text", text_data=msg)
        url: str = self.cfg.url + "/send_group_msg"

        # --- 将 JSON 内的中文等非 ASCII 字符转义成 \uXXXX ---
        # 注意 ensure_ascii=True 才会生成 Unicode 转义
        safe_json = json.dumps(json.loads(send_msg), ensure_ascii=True, indent=2)

        # --- 使用原始 header，不修改全局配置 ---
        header = dict(self.cfg.header)

        print("[send_msg_test] 转义后发送 JSON：")
        print(safe_json, "\nURL:", url)
        print("Header:", header, "\n")

        self._send_request_with_retry(url, safe_json, header)
