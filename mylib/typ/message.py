# OneBot Message 结构体定义
    # - MessageSegment、MessageChain、MessageEvent 等
    # - 用于 build_json() 或其他构造函数
from pydantic import BaseModel, Field, field_validator
from typing import Literal
from .base import BaseMessage

class TextMessageData(BaseModel):
    text:str = Field(..., min_length=1, description="纯文本内容")

    @field_validator("text")
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError("text 内容不能为空")
        return v


class ImageMessageData(BaseModel):
    file: str = Field(..., pattern=r"^https?://", description="图片 URL")

    @field_validator("file")
    def validate_url(cls, v):
        if not v.lower().endswith((".jpg", ".png", ".gif", ".jpeg", "/")):
            raise ValueError("图片 URL 必须是常见图片格式")
        return v


class TextMessage(BaseMessage):
    type: Literal["text"]
    data: TextMessageData


class ImageMessage(BaseMessage):
    type: Literal["image"]
    data: ImageMessageData
