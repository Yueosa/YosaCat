from pydantic import Field, field_validator
from typing import Union
from .base import BaseSend
from .message_types import TextMessage, ImageMessage


Message = Union[TextMessage, ImageMessage]


class SendPrivateMsg(BaseSend):
    """发送私聊消息"""
    user_id: int = Field(..., description="对方 QQ 号")
    message: Message

    @field_validator("user_id")
    def validate_user_id(cls, v):
        if len(str(v)) < 5 or len(str(v)) > 11:
            raise ValueError("user_id 必须是 5~11 位数字")
        return v


class SendGroupMsg(BaseSend):
    """发送群聊消息"""
    group_id: int = Field(..., description="群号")
    message: Message

    @field_validator("group_id")
    def validate_group_id(cls, v):
        if len(str(v)) < 5 or len(str(v)) > 10:
            raise ValueError("group_id 必须是 5~10 位数字")
        return v
