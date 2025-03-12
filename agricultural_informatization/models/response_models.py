from typing import Literal, Union, Optional
from pydantic import BaseModel


class ResponseModel(BaseModel):
    """回复模型"""

    status: Literal["Success", "Fail"]
    """处理状态"""

    msg: str = ""
    """返回消息，失败应返回原因"""

    data: Optional[Union[dict, list, str]] = None
    """数据体，根据接口可能不同"""
