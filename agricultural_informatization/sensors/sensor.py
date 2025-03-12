from typing import Literal, Optional
from abc import ABC, abstractmethod
import paho.mqtt.client
import asyncio
import json

from .config import (
    MQTT_HOST,
    MQTT_PORT,
    MQTT_TOPIC
)
from .log import logger


class Sensor(ABC):
    """模拟传感器类"""

    id: int
    """传感器ID，不同类别相通"""

    field_id: int
    """农田ID"""

    client: Optional[paho.mqtt.client.Client]
    """MQTT Client"""

    type: Literal["soil", "air", "headwaters"]
    """传感器类型，子类应重写该字段"""

    cycle: int = 2
    """发送数据周期，单位为秒"""

    def __init__(self, id: int, field_id: int, cycle: int = 0):
        self.id = id
        self.field_id = field_id
        if cycle > 0:
            self.cycle = cycle
        self.connect()
        logger.info(f"{self.type} 传感器初始化完成，传感器ID {self.id}，农田ID {self.field_id}，数据发送周期 {self.cycle}")

    @abstractmethod
    def simulate_data(self) -> dict:
        """重写数据模拟方法"""

    def connect(self):
        """连接 MQTT 服务器，并将客户端对象存入 self.client"""
        client = paho.mqtt.client.Client(
            paho.mqtt.client.CallbackAPIVersion.VERSION2  # type:ignore
        )
        try:
            client.connect(MQTT_HOST, MQTT_PORT)
            self.client = client
        except:
            logger.warning(f"{self.type} 传感器初始化失败，传感器ID {self.id}，农田ID {self.field_id}，数据发送周期 {self.cycle}")
            self.client = None

    async def run(self):
        """开始定期发送信息"""
        if self.client is None:
            logger.warning(f"{self.type} 传感器 {self.id} 未正常连接至 MQTT 服务器，已忽略。")
            return
        while True:
            data = self.simulate_data()
            try:
                self.client.publish(
                    topic=MQTT_TOPIC,
                    payload=json.dumps(data),
                )
            except:
                logger.error(f"{self.type} 传感器 {self.id} 发送数据失败。")
            else:
                logger.debug(f"{self.type} 传感器 {self.id} 发送数据：{data}")
            await asyncio.sleep(self.cycle)
