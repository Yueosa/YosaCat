import sys, os
sys.path.append(os.path.dirname(__file__))

from TYP import *

import json

from typing import Literal


def _build_json(data: dict) -> str:
    """转为JSON字符串"""
    return data.model_dump_json(indent=2, ensure_ascii=False)

def _text_message():
    pass

def image_message():
    pass

def build_group_message(
        group_id: int,
        mode: Literal["text", "image"],
        text_data: str = "miss you~",
        image_file_data: str = "https://www.loliapi.com/bg/",
) -> str:
    if mode == "text":
        msg = TextMessage(type="text", data=TextMessageData(text=text_data))

    if mode == "image":
        msg = ImageMessage(type="image", data=ImageMessageData(file=image_file_data))

    data: SendGroupMsg = SendGroupMsg(
        group_id=group_id,
        message=msg
    )
    return _build_json(data)
