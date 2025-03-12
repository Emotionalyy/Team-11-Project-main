"""农田信息模型"""

from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import date


class FieldInfo(BaseModel):
    """农田信息模型"""

class FieldSoilInfo(BaseModel):
    """土壤传感器数据"""

    field_id: int
    """农田ID"""

    time: Optional[int]
    """检测时间戳"""

    moisture: Optional[float]
    """土壤湿度"""

class FieldAirInfo(BaseModel):
    """空气传感器数据"""

    field_id: int
    """农田ID"""

    time: Optional[int]
    """检测时间戳"""

    humidity: Optional[float]
    """空气湿度"""

    temperature: Optional[float]
    """空气温度"""

class FieldHeadwatersInfo(BaseModel):
    """水源检测传感器数据"""

    field_id: int
    """农田ID"""

    time: Optional[int]
    """检测时间戳"""

    ph: Optional[float]
    """水源pH值"""

    hardness: Optional[float]
    """水源硬度"""

    solids: Optional[float]
    """总溶解固体"""

    chloramines: Optional[float]
    """氯胺"""

    sulfate: Optional[float]
    """硫酸盐"""

    conductivity: Optional[float]
    """电导率"""

    organic_carbon: Optional[float]
    """有机碳"""

    trihalomethanes: Optional[float]
    """三卤甲烷"""

    turbidity: Optional[float]
    """浊度"""

    potability: Optional[bool]
    """可饮用性"""

class FertilizationInfo(BaseModel):
    """施肥事件信息"""

    user_id: int
    """施肥用户ID"""

    field_id: int
    """农田ID"""

    date: date
    """施肥日期"""

    type: str
    """肥料种类"""

    density: float
    """施肥密度，kg/公顷"""

    note: str
    """备注信息"""


class FieldSingleForm(BaseModel):
    """查询单块农田的传感器数据表单"""

    field_id: int
    """农田ID"""

    limit: int = 50
    """限制数据条数"""

    @model_validator(mode="after")
    def limit_checker(self):
        if self.limit <= 0:
            self.limit = 50
        return self

class AddFertilizationForm(BaseModel):
    """添加施肥事件表单"""

    user_id: int
    """发起请求的用户ID"""

    data: FertilizationInfo
    """施肥事件信息"""


class SearchFertilizationConditionForm(BaseModel):
    """农田信息搜索的筛选条件"""

    user_id: Optional[int] = None
    """施肥用户ID"""

    field_id: Optional[int] = None
    """农田ID"""

    start_date: Optional[date] = None
    """施肥开始日期"""

    end_date: Optional[date] = None
    """施肥结束日期"""

    type: Optional[str] = None
    """肥料种类"""

    min_density: Optional[float] = None
    """最小施肥密度，kg/公顷"""

    max_density: Optional[float] = None
    """最大施肥密度，kg/公顷"""

class SearchFertilizationForm(BaseModel):
    """添加施肥事件表单"""

    user_id: int
    """发起请求的用户ID"""

    search_condition: SearchFertilizationConditionForm
    """搜索施肥事件条件"""

    number_limit: Optional[int] = 50
    """搜索数量限制"""