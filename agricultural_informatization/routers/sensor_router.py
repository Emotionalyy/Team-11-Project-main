from fastapi import APIRouter, Body
from typing import Annotated

from models.response_models import ResponseModel
from models.sensor_models import *
from utils import execute_sql
from utils import logger

router = APIRouter()


def nodata_return(router):
    logger.debug(f"\t/sensor{router}\t数据库中无传感器信息")
    return ResponseModel(
        status="Fail",
        msg="数据库中无传感器信息"
    )


@router.post("/status", summary="查询所有传感器信息")
async def _():
    logger.info("\t/sensor/status\t查询所有传感器信息")
    data = execute_sql(
        """
    SELECT 
        Sensors.sensor_id,
        Sensors.name,
        Sensors.field_id,
        Sensors.type,
        Sensors.status,
        Sensor_Maintenance.date
    FROM Sensors
         LEFT JOIN(SELECT sensor_id, MAX(date) AS max_date
                   FROM Sensor_Maintenance
                   GROUP BY sensor_id) AS Latest_Maintenance ON Sensors.sensor_id = Latest_Maintenance.sensor_id
         LEFT JOIN Sensor_Maintenance ON Latest_Maintenance.sensor_id = Sensor_Maintenance.sensor_id AND
                                         Latest_Maintenance.max_date = Sensor_Maintenance.date;
        """
    )
    if len(data) == 0:
        return nodata_return("status")
    res = []
    for single in data:
        res.append(SensorInfo(
            sensor_id=single[0],
            name=single[1],
            field_id=single[2],
            type=single[3],
            status=single[4],
            date=single[5])
        )
    logger.info("\t/sensor/status\t查询成功")
    return ResponseModel(
        status="Success",
        msg="查询成功",
        data=res
    )


@router.post("/status_single", summary="查询单个传感器信息")
async def _(sensor_id: Annotated[int, Body(embed=True)]):
    logger.info(f"\t/sensor/status_single\t查询传感器, sensor_id = {sensor_id}")
    data = execute_sql(
        f"""
        SELECT Sensors.sensor_id,
            Sensors.name,
            Sensors.field_id,
            Sensors.type,
            Sensors.status,
            Sensor_Maintenance.date
        FROM Sensors
             LEFT JOIN(SELECT sensor_id, MAX(date) AS max_date
                       FROM Sensor_Maintenance
                       GROUP BY sensor_id) AS Latest_Maintenance ON Sensors.sensor_id = Latest_Maintenance.sensor_id
             LEFT JOIN Sensor_Maintenance ON Latest_Maintenance.sensor_id = Sensor_Maintenance.sensor_id AND
                                             Latest_Maintenance.max_date = Sensor_Maintenance.date
        where  Sensors.sensor_id = {sensor_id};
        """
    )
    if len(data) == 0:
        return nodata_return("status_single")
    else:
        res = []
        for single in data:
            res.append(SensorInfo(
                sensor_id=single[0],
                name=single[1],
                field_id=single[2],
                type=single[3],
                status=single[4],
                date=single[5])
            )
        logger.info(f"\t/sensor/status_single\t查询成功")
        return ResponseModel(
            status="Success",
            msg="查询成功",
            data=res
        )


@router.post("/add", summary="添加传感器")
async def _(form: SensorAddForm):
    logger.info("\t/sensor/add\t添加传感器:", form)
    # 限定农田id必须为已经存在的
    data = execute_sql(
        f"SELECT DISTINCT field_id FROM Fields;"
    )
    fields_id = [x[0] for x in data]
    if form.field_id not in fields_id:
        logger.debug("\t/sensor/add\t所添加传感器的农田id（外键）不存在，添加失败")
        return ResponseModel(
            status="Fail",
            msg="所添加传感器的农田id（外键）不存在，添加失败"
        )
    try:
        execute_sql(
            f"""INSERT INTO Sensors (sensor_id, name, field_id, type, status) 
            VALUES (0,'{form.name}', {form.field_id},'{form.type}',{form.status});"""
        )
        logger.info("\t/sensor/add\t添加成功")
        return ResponseModel(
            status="Success",
            msg="添加成功"
        )
    except Exception as e:
        logger.warning("\t/sensor/add\t添加错误")
        return ResponseModel(status="Fail", msg=str(e))


@router.post("/delete", summary="删除传感器")
async def _(sensor_id: Annotated[int, Body(embed=True)]):
    logger.debug(f"\t/sensor/delete\t删除传感器 sensor_id = {sensor_id}")
    data = execute_sql(
        f"SELECT * FROM Sensors WHERE sensor_id = {sensor_id};"
    )
    if len(data) == 0:
        return nodata_return("delete")
    else:
        try:
            execute_sql(
                f"DELETE FROM Sensor_Maintenance WHERE sensor_id={sensor_id};"
            )
            execute_sql(
                f"DELETE FROM Sensors WHERE sensor_id={sensor_id};"
            )
            logger.info(f"\t/sensor/delete\t删除成功")
            return ResponseModel(
                status="Success",
                msg="删除成功",
            )
        except Exception as e:
            logger.warning(f"\t/sensor/delete\t删除错误")
            raise
            return ResponseModel(code="Fail", msg=str(e))


@router.post("/update", summary="编辑传感器信息")
async def _(form: SensorEditForm):
    logger.debug(f"\t/sensor/update\t编辑传感器:{form}")
    data = execute_sql(f"SELECT * FROM Sensors WHERE sensor_id={form.sensor_id};")
    if len(data) == 0:
        return nodata_return("update")
    else:
        try:
            if form.name is not None:
                execute_sql(
                    f"UPDATE Sensors SET name='{form.name}' WHERE sensor_id={form.sensor_id};"
                )
            if form.type is not None:
                execute_sql(
                    f"UPDATE Sensors SET type='{form.type}' WHERE sensor_id={form.sensor_id};"
                )
            if form.status is not None:
                execute_sql(
                    f"UPDATE Sensors SET status={form.status} WHERE sensor_id={form.sensor_id};"
                )
            if form.date is not None:
                data = execute_sql(
                    f"SELECT * FROM Sensor_Maintenance WHERE sensor_id = {form.sensor_id};"
                )
                if len(data) != 0:
                    execute_sql(
                        f"UPDATE Sensor_Maintenance SET date='{form.date}' WHERE sensor_id={form.sensor_id};"
                    )
                else:
                    execute_sql(
                        f"INSERT INTO Sensor_Maintenance (id, sensor_id, date) VALUES (0, {form.sensor_id}, '{form.date}');"
                    )
            logger.info("\t/sensor/update\t编辑成功")
            return ResponseModel(
                status="Success",
                msg="修改成功",
            )
        except Exception as e:
            logger.warning("\t/sensor/update\t编辑错误")
            return ResponseModel(status="Fail", msg=str(e))


@router.post("/historical_monitoring_single_data", summary="查询传感器设备历史检测数据")
async def _(sensor_id: Annotated[int, Body()], limit: Annotated[int, Body()] = 50):
    logger.info(
        f"\t/sensor/historical_monitoring_single_data\t查询传感器设备历史运行数据, sensor_id = {sensor_id}")
    # 查询field_id
    data = execute_sql(
        f"""
            SELECT field_id
            FROM Sensors
            WHERE sensor_id = {sensor_id};
        """
    )
    if len(data) == 0:
        return nodata_return("historical_monitoring_single_data")
    field_id = data[0][0]

    # 查询type
    type = execute_sql(
        f"""
            SELECT type
            FROM Sensors
            WHERE sensor_id = {sensor_id};
        """
    )[0][0]

    # 查询name
    name = execute_sql(
        f"""
            SELECT name
            FROM Sensors
            WHERE sensor_id = {sensor_id};
        """
    )[0][0]

    # 查询传感器历史运行数据
    res = []
    if type == 'soil':
        data = execute_sql(
            f"""
                SELECT 
                `field_id`,
                UNIX_TIMESTAMP(`time`) AS '',
                `moisture`
                FROM Soil_Status
                WHERE field_id = {field_id}
                ORDER BY time DESC
                LIMIT {limit};
            """
        )
        for single in data:
            res.append(SensorSoilInfo(
                sensor_id=sensor_id,
                name=name,
                time=single[1],
                field_id=single[0],
                moisture=single[2]
            ))
    elif type == 'air':
        data = execute_sql(
            f"""
                SELECT 
                `field_id`,
                UNIX_TIMESTAMP(`time`) AS '',
                `humidity`,
                `temperature`
                FROM Air_Status
                WHERE field_id = {field_id}
                ORDER BY time DESC
                LIMIT {limit};
            """
        )
        for single in data:
            res.append(SensorAirInfo(
                sensor_id=sensor_id,
                name=name,
                time=single[1],
                field_id=single[0],
                humidity=single[2],
                temperature=single[3]
            ))
    elif type == 'headwaters':
        data = execute_sql(
            f"""
                SELECT 
                `field_id`,
                UNIX_TIMESTAMP(`time`) AS '',
                `ph`,
                `hardness`,
                `solids`,
                `chloramines`,
                `sulfate`,
                `conductivity`,
                `organic_carbon`,
                `trihalomethanes`,
                `turbidity`,
                `potability`
                FROM Headwaters_Status
                WHERE field_id = {field_id}
                ORDER BY time DESC
                LIMIT {limit};
            """
        )
        for single in data:
            res.append(SensorHeadwatersInfo(
                sensor_id=sensor_id,
                name=name,
                time=single[1],
                field_id=single[0],
                ph=single[2],
                hardness=single[3],
                solids=single[4],
                chloramines=single[5],
                sulfate=single[6],
                conductivity=single[7],
                organic_carbon=single[8],
                trihalomethanes=single[9],
                turbidity=single[10],
                potability=single[11]
            ))
    logger.info(
        f"\/sensor/sensor/historical_monitoring_single_data\t查询成功")
    return ResponseModel(
        status="Success",
        msg="查询成功",
        data=res
    )


@router.post("/historical_maintenance_single_data", summary="查询单个传感器时间段测量数据")
async def _(sensor_id: Annotated[int, Body()], limit: Annotated[int, Body()] = 10):
    logger.info(f"\t/sensor/historical_maintenance_single_data\t查询传感器, sensor_id = {sensor_id}")
    data = execute_sql(
        f"SELECT * FROM Sensor_Maintenance WHERE sensor_id = {sensor_id};"
    )
    if len(data) == 0:
        return nodata_return("historical_maintenance_single_data")
    else:
        data = execute_sql(
            f"""
                SELECT `id`,
                       `sensor_id`,
                       `date`
                FROM Sensor_Maintenance
                WHERE sensor_id = {sensor_id}
                ORDER BY date DESC
                LIMIT {limit};
            """
        )
        res = []
        for single in data:
            res.append(SensorMaintHistoryInfo(
                id=single[0],
                sensor_id=single[1],
                date=single[2]
            ))
        logger.info(f"\t/sensor/historical_maintenance_single_data\t查询成功")
        return ResponseModel(
            status="Success",
            msg="查询成功",
            data=res
        )


@router.post("/during_monitoring_single_data", summary="查询单个传感器时间段测量数据")
async def _(sensor_id: Annotated[int, Body()], start_time: Annotated[int, Body()],
            end_time: Annotated[int, Body()] = int(int(datetime.datetime.now().timestamp()))):
    logger.info(
        f"\t/sensor/during_monitoring_single_data\t查询单个传感器时间段测量数据, sensor_id = {sensor_id}")

    # 判断开始时间与结束时间是否合法
    if start_time > 0 and end_time > 0:
        if start_time > end_time:
            logger.debug(
                f"\t/sensor/during_monitoring_single_data\tstart_time > end_time 不合法")
            return ResponseModel(
                status="Fail",
                msg="start_time > end_time 不合法"
            )
    else:
        logger.debug(
            f"\t/sensor/during_monitoring_single_data\t开始时间与结束时间不合法")
        return ResponseModel(
            status="Fail",
            msg="start_time 或 end_time < 0 不合法"
        )

    # 查询field_id
    data = execute_sql(
        f"""
            SELECT field_id
            FROM Sensors
            WHERE sensor_id = {sensor_id};
        """
    )
    if len(data) == 0:
        return nodata_return("during_monitoring_single_data")
    field_id = data[0][0]

    # 查询type
    type = execute_sql(
        f"""
            SELECT type
            FROM Sensors
            WHERE sensor_id = {sensor_id};
        """
    )[0][0]

    # 查询name
    name = execute_sql(
        f"""
            SELECT name
            FROM Sensors
            WHERE sensor_id = {sensor_id};
        """
    )[0][0]

    # 查询传感器历史运行数据
    res = []
    if type == 'soil':
        data = execute_sql(
            f"""
                SELECT 
                `field_id`,
                UNIX_TIMESTAMP(`time`) AS 'timestamp',
                `moisture`
                FROM Soil_Status
                WHERE `field_id` = {field_id}
                  AND UNIX_TIMESTAMP(`time`) BETWEEN {start_time} AND {end_time}
                ORDER BY `time` DESC;
            """
        )
        for single in data:
            res.append(SensorSoilInfo(
                sensor_id=sensor_id,
                name=name,
                time=single[1],
                field_id=single[0],
                moisture=single[2]
            ))
    elif type == 'air':
        data = execute_sql(
            f"""
                SELECT 
                `field_id`,
                UNIX_TIMESTAMP(`time`) AS '',
                `humidity`,
                `temperature`
                FROM Air_Status
                WHERE `field_id` = {field_id}
                  AND UNIX_TIMESTAMP(`time`) BETWEEN {start_time} AND {end_time}
                ORDER BY `time` DESC;
            """
        )
        for single in data:
            res.append(SensorAirInfo(
                sensor_id=sensor_id,
                name=name,
                time=single[1],
                field_id=single[0],
                humidity=single[2],
                temperature=single[3]
            ))
    elif type == 'headwaters':
        data = execute_sql(
            f"""
                SELECT 
                `field_id`,
                UNIX_TIMESTAMP(`time`) AS '',
                `ph`,
                `hardness`,
                `solids`,
                `chloramines`,
                `sulfate`,
                `conductivity`,
                `organic_carbon`,
                `trihalomethanes`,
                `turbidity`,
                `potability`
                FROM Headwaters_Status
                WHERE `field_id` = {field_id}
                  AND UNIX_TIMESTAMP(`time`) BETWEEN {start_time} AND {end_time}
                ORDER BY `time` DESC;
            """
        )
        for single in data:
            res.append(SensorHeadwatersInfo(
                sensor_id=sensor_id,
                name=name,
                time=single[1],
                field_id=single[0],
                ph=single[2],
                hardness=single[3],
                solids=single[4],
                chloramines=single[5],
                sulfate=single[6],
                conductivity=single[7],
                organic_carbon=single[8],
                trihalomethanes=single[9],
                turbidity=single[10],
                potability=single[11]
            ))
    logger.info(
        f"\t/sensor/during_monitoring_single_data\t查询成功")
    return ResponseModel(
        status="Success",
        msg="查询成功",
        data=res
    )
