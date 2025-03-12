from pydantic import BaseModel
from typing import Optional
from datetime import date


class AgriMachInfo(BaseModel):
    """农机数据"""

    mach_id: int
    """农机ID"""

    name: str
    """农机名称"""

    usage: str
    """农机用处"""

    mach_status: bool
    """农机状态，是否正在使用"""

    last_main_date: Optional[date]
    """农机上次维护日期"""

    last_used_date: Optional[date]
    """上次使用日期"""

class AgriMachUseInfo(BaseModel):
    """农机使用事件数据"""

    mach_id: int
    """农机ID"""

    user_id: int
    """施肥用户ID"""

    date: date
    """农机使用日期"""

    note: str
    """备注信息"""

    main_status: bool
    """当次使用后是否进行维护"""

class AddAgriMachUseForm(BaseModel):
    """农机使用数据表单"""

    user_id: int
    """发起请求的用户ID"""

    data: AgriMachUseInfo
    """农机使用事件信息"""