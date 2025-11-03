# 消息分发调度器
    # - 接收 Parser 层返回的结构体
    # - 调用对应 Command 层或插件
from fastapi import Request

from message_sender import MessageSender

from message_excute import execute_command

class Cerebrum:
    def __init__(self):
        self.msgsdr = MessageSender()

    def command_mind(self, data: Request):
        flag = 1
        if self._get_id(data) in self.msgsdr.cfg.group:
            if self._get_text(data) in self.msgsdr.cfg.message_list:
                self.msgsdr.send_group_msg(self._get_id(data))
                flag = 0
            if self._get_text(data) in self.msgsdr.cfg.image_list:
                self.msgsdr.send_group_img(self._get_id(data))
                flag = 0
            if self._get_text(data) in self.msgsdr.cfg.test_list:
                self.msgsdr.send_group_img_loli(self._get_id(data))
                flag = 0
            if self._get_text(data) == "<yb> -p x --output all":
                # text = self.yb()
                text = "Query Successful"
                test_text = "测试中文"
                self.msgsdr.send_msg(self._get_id(data), f"{text}")
                self.msgsdr.send_msg_test(self._get_id(data), f"{test_text}")
                flag = 0
                
            if flag:
                print(data)
                print(self._get_text(data))
                name, parma = execute_command(self._get_text(data))
                print(name, "\n\n", parma)
                self.msgsdr.send_msg_test(self._get_id(data), f"{name}: {parma}")
            
    def _get_id(self, data: dict) -> str | None:
        try:
            return data["group_id"]
        except (KeyError, IndexError, TypeError):
            return None

    def _get_text(self, data: dict) -> str | None:
        try:
            return str(data["message"][0]["data"]["text"])
        except (KeyError, IndexError, TypeError):
            return None