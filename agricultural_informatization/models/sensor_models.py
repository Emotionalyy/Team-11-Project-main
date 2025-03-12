"""传感器信息模型"""
from pydantic import BaseModel
from typing import Literal, Optional
import datetime


class SensorInfo(BaseModel):
    """传感器信息类"""
    sensor_id: int
    """传感器ID"""

    name: str = ""
    """传感器名称"""

    field_id: int
    """农田ID"""

    type: Literal["soil", "air", "headwaters"]
    """传感器类型"""

    status: bool = True
    """传感器状态"""

    date: Optional[datetime.date] = None
    """传感器维护时间"""


class SensorAddForm(BaseModel):
    """添加传感器类"""

    name: str = ""
    """传感器名称"""

    field_id: int
    """农田ID"""

    type: Literal["soil", "air", "headwaters"]
    """传感器类型"""

    status: bool = True
    """传感器状态"""


class SensorEditForm(BaseModel):
    """编辑传感器类"""
    sensor_id: int
    """传感器ID"""

    name: str = ""
    """传感器名称"""

    type: Literal["soil", "air", "headwaters"]
    """传感器类型"""

    status: bool = True
    """传感器状态"""

    date: Optional[datetime.date] = None
    """传感器维护时间"""


class SensorSoilInfo(BaseModel):
    """农田土壤传感器数据"""
    sensor_id: int
    """传感器ID"""

    name: str = ""
    """传感器名称"""

    time: int
    """采集时间"""

    field_id: int
    """农田ID"""

    moisture: float
    """土壤湿度"""


class SensorAirInfo(BaseModel):
    """农田空气传感器数据"""
    sensor_id: int
    """传感器ID"""

    name: str = ""
    """传感器名称"""

    time: int
    """采集时间"""

    field_id: int
    """农田ID"""

    humidity: float
    """空气湿度"""

    temperature: float
    """空气温度"""


class SensorHeadwatersInfo(BaseModel):
    """农田水源传感器数据"""
    sensor_id: int
    """传感器ID"""

    name: str = ""
    """传感器名称"""

    time: int
    """采集时间"""

    field_id: int
    """农田ID"""

    ph: float
    """水源pH值"""

    hardness: float
    """水源硬度"""

    solids: float
    """总溶解固体"""

    chloramines: float
    """氯胺"""

    sulfate: float
    """硫酸盐"""

    conductivity: float
    """电导率"""

    organic_carbon: float
    """有机碳"""

    trihalomethanes: float
    """三卤甲烷"""

    turbidity: float
    """浊度"""

    potability: bool
    """可饮用性"""

class SensorMaintHistoryInfo(BaseModel):
    """传感器信息类"""
    id: int
    """传感器维护事件递增ID"""

    sensor_id: int
    """传感器ID"""

    date: Optional[datetime.date] = None
    """传感器维护时间"""