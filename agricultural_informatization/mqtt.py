import paho.mqtt.client
from typing import cast

from models.sensor_data_models import (
    SensorDataModel,
    AirSensorDataContent,
    SoilSensorDataContent,
    HeadwatersSensorDataContent
)
from utils import logger, config, EXIT_HOOK_FUNCS, execute_sql


def on_connect(
        client: paho.mqtt.client.Client,
        userdata,
        flags,
        reason_code,
        properties
    ):
    """连接 MQTT 服务器回调函数"""
    logger.info(f"订阅端连接 MQTT 服务器完成，结果码：{reason_code}")
    client.subscribe(config.MQTT_TOPIC)

def on_message(
        client: paho.mqtt.client.Client,
        userdata,
        msg: paho.mqtt.client.MQTTMessage
    ):
    """接收到 MQTT 消息回调函数"""
    sensor_data = SensorDataModel.model_validate_json(
        msg.payload
    )
    logger.debug(f"MQTT 接收到来自 {sensor_data.type} 传感器 {sensor_data.id} 的消息：{sensor_data.model_dump()}")
    # 检查传感器数据
    check_data = execute_sql(
        f"""
        SELECT COUNT(*) FROM Sensors WHERE sensor_id={sensor_data.id} AND field_id={sensor_data.field_id} AND type='{sensor_data.type}' AND status=1;
        """
    )
    if check_data[0][0] == 0:
        logger.warning(f"未找到相应传感器，请检查数据库信息是否正确：负责 {sensor_data.field_id} 农田的{sensor_data.type} 传感器 {sensor_data.id}")
        return
    try:
        if sensor_data.type == "air":
            sensor_data.data = cast(AirSensorDataContent, sensor_data.data)
            execute_sql(
                f"""
                INSERT INTO Air_Status 
                VALUES({sensor_data.field_id}, FROM_UNIXTIME({sensor_data.time}), {sensor_data.data.humidity}, {sensor_data.data.temperature});
                """
            )
        elif sensor_data.type == "soil":
            sensor_data.data = cast(SoilSensorDataContent, sensor_data.data)
            execute_sql(
                f"""
                INSERT INTO Soil_Status 
                VALUES({sensor_data.field_id}, FROM_UNIXTIME({sensor_data.time}), {sensor_data.data.moisture});
                """
            )
        elif sensor_data.type == "headwaters":
            sensor_data.data = cast(HeadwatersSensorDataContent, sensor_data.data)
            execute_sql(
                f"""
                INSERT INTO Headwaters_Status 
                VALUES(
                    {sensor_data.field_id},
                    FROM_UNIXTIME({sensor_data.time}),
                    {sensor_data.data.ph},
                    {sensor_data.data.hardness},
                    {sensor_data.data.solids},
                    {sensor_data.data.chloramines},
                    {sensor_data.data.sulfate},
                    {sensor_data.data.conductivity},
                    {sensor_data.data.organic_carbon},
                    {sensor_data.data.trihalomethanes},
                    {sensor_data.data.turbidity},
                    {1 if sensor_data.data.potability else 0}
                );
                """
            )
    except Exception as e:
        logger.error(f"传感器数据插入数据库时出错：{e}")
        return
    logger.success("传感器数据保存成功。")


mqttc = paho.mqtt.client.Client(paho.mqtt.client.CallbackAPIVersion.VERSION2) # type: ignore
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect(
    host=config.MQTT_HOST,
    port=config.MQTT_PORT
)
mqttc.loop_start()
EXIT_HOOK_FUNCS.append(mqttc.loop_stop)


__all__ = [
    "mqttc"
]