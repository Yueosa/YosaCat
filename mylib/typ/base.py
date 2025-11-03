# 基础数据类型（用于 model_dump_json、Pydantic 模型基类）
# - 提供统一的序列化、校验、可扩展字段支持
from pydantic import BaseModel


class BaseSend(BaseModel):
    """所有发送类型的通用字段"""
    auto_escape: bool = False

    class Config:
        populate_by_name = False
        extra = "ignore"


class BaseMessage(BaseModel):
    """消息基类"""
    type: str

    class Config:
        populate_by_name = False
        extra = "forbid"
