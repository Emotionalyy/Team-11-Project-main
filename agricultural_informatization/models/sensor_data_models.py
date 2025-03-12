from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Literal, Union


class SoilSensorDataContent(BaseModel):
    """农田土壤传感器数据"""

    moisture: float
    """土壤湿度"""


class AirSensorDataContent(BaseModel):
    """农田空气传感器数据"""

    humidity: float
    """空气湿度"""

    temperature: float
    """空气温度"""


class HeadwatersSensorDataContent(BaseModel):
    """农田水源传感器数据"""

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


class SensorDataModel(BaseModel):
    """传感器数据类"""

    id: int
    """传感器ID"""

    field_id: int
    """农田ID"""

    type: Literal["soil", "air", "headwaters"]
    """传感器类型"""

    time: int
    """检测时间戳，10位数字"""

    data: Union[SoilSensorDataContent, AirSensorDataContent, HeadwatersSensorDataContent] = Field(union_mode="smart")
    """传感器数据"""

    @model_validator(mode="after")
    def _(self):
        if self.type == "soil" and isinstance(self.data, SoilSensorDataContent):
            return self
        if self.type == "air" and isinstance(self.data, AirSensorDataContent):
            return self
        if self.type == "headwaters" and isinstance(self.data, HeadwatersSensorDataContent):
            return self
        raise ValidationError
