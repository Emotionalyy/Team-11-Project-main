import asyncio

from .headwaters import Headwaters
from .sensor import Sensor
from .soil import Soil
from .air import Air


sensor_ls = {
    "headwaters": [(1, 1), (2, 2), (3, 3), (10, 4), (11, 5), (12, 6), (13, 7), (14, 8)],
    "air": [(4, 1), (5, 2), (6, 3), (15, 5), (16, 7), (17, 8), (18, 9)],
    "soil": [(7, 1), (8, 2), (9, 3), (19, 4), (20, 5), (21, 6), (22, 7), (23, 8), (24, 9)]
}

sensors: list[Sensor] = []

for k, ls in sensor_ls.items():
    if k == "headwaters":
        sensor_cls = Headwaters
        cycle = 30
    elif k == "air":
        sensor_cls = Air
        cycle = 20
    else:
        sensor_cls = Soil
        cycle = 20
    
    for id, field_id in ls:
        sensors.append(
            sensor_cls(id, field_id, cycle)
        )

async def main():
    await asyncio.gather(
        *[sensor.run() for sensor in sensors]
    )