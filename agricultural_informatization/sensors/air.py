from typing_extensions import override
import datetime

from .models import AirSensorDataContent, SensorDataModel, SmoothRandom
from .sensor import Sensor


class Air(Sensor):
    """空气传感器（数据模拟）"""

    type = "air"

    # 初始化平滑随机数生成器
    humidity_gen = SmoothRandom(initial_value=0.5, min_value=0, max_value=1)
    temperature_gen = SmoothRandom(initial_value=20, min_value=10, max_value=50)

    @override
    def simulate_data(self) -> dict:
        data_model = AirSensorDataContent(
            humidity=self.humidity_gen.next(),
            temperature=self.temperature_gen.next()
        )
        return SensorDataModel(
            id=self.id,
            field_id=self.field_id,
            type=self.type,
            time=round(datetime.datetime.timestamp(datetime.datetime.now())),
            data=data_model
        ).model_dump()
