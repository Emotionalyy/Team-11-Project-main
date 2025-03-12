from typing_extensions import override
import datetime
import random

from .models import SoilSensorDataContent, SensorDataModel, SmoothRandom
from .sensor import Sensor


class Soil(Sensor):
    """土壤传感器（数据模拟）"""

    type = "soil"

    # 初始化平滑随机数生成器
    moisture_gen = SmoothRandom(initial_value=0.75, min_value=0.5, max_value=0.75)

    @override
    def simulate_data(self) -> dict:
        data_model = SoilSensorDataContent(
            moisture=self.moisture_gen.next()
        )
        return SensorDataModel(
            id=self.id,
            field_id=self.field_id,
            type=self.type,
            time=round(datetime.datetime.timestamp(datetime.datetime.now())),
            data=data_model
        ).model_dump()
