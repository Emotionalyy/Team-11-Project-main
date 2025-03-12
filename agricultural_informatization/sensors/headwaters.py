from typing_extensions import override
import datetime
import random

from .models import HeadwatersSensorDataContent, SensorDataModel, SmoothRandom
from .sensor import Sensor


class Headwaters(Sensor):
    """水源传感器（数据模拟）"""

    type = "headwaters"

    # 初始化平滑随机数生成器
    ph_gen = SmoothRandom(initial_value=6.5, min_value=3, max_value=10)
    hardness_gen = SmoothRandom(initial_value=100, min_value=0, max_value=200)
    solids_gen = SmoothRandom(initial_value=250, min_value=0, max_value=500)
    chloramines_gen = SmoothRandom(initial_value=5, min_value=0, max_value=10)
    sulfate_gen = SmoothRandom(initial_value=50, min_value=0, max_value=100)
    conductivity_gen = SmoothRandom(initial_value=1000, min_value=0, max_value=2000)
    organic_carbon_gen = SmoothRandom(initial_value=25, min_value=0, max_value=50)
    trihalomethanes_gen = SmoothRandom(initial_value=50, min_value=0, max_value=100)
    turbidity_gen = SmoothRandom(initial_value=2.5, min_value=0, max_value=5)

    @override
    def simulate_data(self):
        data_model = HeadwatersSensorDataContent(
            ph=self.ph_gen.next(),
            hardness=self.hardness_gen.next(),
            solids=self.solids_gen.next(),
            chloramines=self.chloramines_gen.next(),
            sulfate=self.sulfate_gen.next(),
            conductivity=self.conductivity_gen.next(),
            organic_carbon=self.organic_carbon_gen.next(),
            trihalomethanes=self.trihalomethanes_gen.next(),
            turbidity=self.turbidity_gen.next(),
            potability=random.choice([False, True])
        )
        return SensorDataModel(
            id=self.id,
            field_id=self.field_id,
            type=self.type,
            time=round(datetime.datetime.timestamp(datetime.datetime.now())),
            data=data_model
        ).model_dump()
