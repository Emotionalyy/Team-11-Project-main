from fastapi import APIRouter

from models.response_models import ResponseModel
from models.field_models import (
    FieldAirInfo,
    FieldSoilInfo,
    FieldHeadwatersInfo,
    FieldSingleForm
)
from utils import execute_sql


router = APIRouter()

@router.post("/soil_info", summary="查询各农田土壤传感器数据")
async def _():
    sql_data = execute_sql(
        """
        SELECT 
            field_id,
            time,
            moisture
        FROM (
            SELECT
                f.field_id AS `field_id`,
                UNIX_TIMESTAMP(soil_s.time) AS `time`,
                soil_s.moisture AS `moisture`,
                RANK() OVER (PARTITION BY f.field_id ORDER BY soil_s.time DESC) AS `rank`
            FROM Fields f LEFT JOIN Soil_Status soil_s ON (f.field_id = soil_s.field_id)
            ) tmp
        WHERE tmp.rank = 1;
        """
    )
    res = []
    for data in sql_data:
        res.append(
            FieldSoilInfo(
                field_id=data[0],
                time=data[1],
                moisture=data[2]
            ).model_dump()
        )
    return ResponseModel(
        status="Success",
        msg="查询成功",
        data=res
    )


@router.post("/soil_info_single", summary="查询单个农田的最新土壤传感器数据")
async def _(form: FieldSingleForm):
    count_data = execute_sql(
        f"""
        SELECT COUNT(*)
        FROM Fields f
        WHERE f.field_id = {form.field_id};
        """
    )
    if count_data[0][0] == 0:
        return ResponseModel(
            status="Fail",
            msg="所查询的农田不存在"
        )
    sql_data = execute_sql(
        f"""
        SELECT
            field_id,
            UNIX_TIMESTAMP(time) AS `time`,
            moisture
        FROM Soil_Status soil_s
        WHERE soil_s.field_id = {form.field_id}
        ORDER BY time DESC
        LIMIT {form.limit};
        """
    )
    res = []
    for data in sql_data:
        res.append(
            FieldSoilInfo(
                field_id=data[0],
                time=data[1],
                moisture=data[2]
            ).model_dump()
        )
    return ResponseModel(
        status="Success",
        msg="查询成功",
        data=res
    )


@router.post("/air_info", summary="查询各农田空气传感器数据")
async def _():
    sql_data = execute_sql(
        """
        SELECT 
            field_id,
            time,
            humidity,
            temperature
        FROM (
            SELECT
                f.field_id AS `field_id`,
                UNIX_TIMESTAMP(air_s.time) AS `time`,
                air_s.humidity AS `humidity`,
                air_s.temperature AS `temperature`,
                RANK() OVER (PARTITION BY f.field_id ORDER BY air_s.time DESC) AS `rank`
            FROM Fields f LEFT JOIN Air_Status air_s ON (f.field_id = air_s.field_id)
            ) tmp
        WHERE tmp.rank = 1;
        """
    )
    res = []
    for data in sql_data:
        res.append(
            FieldAirInfo(
                field_id=data[0],
                time=data[1],
                humidity=data[2],
                temperature=data[3]
            ).model_dump()
        )
    return ResponseModel(
        status="Success",
        msg="查询成功",
        data=res
    )


@router.post("/air_info_single", summary="查询单个农田的最新空气传感器数据")
async def _(form: FieldSingleForm):
    count_data = execute_sql(
        f"""
        SELECT COUNT(*)
        FROM Fields f
        WHERE f.field_id = {form.field_id};
        """
    )
    if count_data[0][0] == 0:
        return ResponseModel(
            status="Fail",
            msg="所查询的农田不存在"
        )
    sql_data = execute_sql(
        f"""
        SELECT
            field_id,
            UNIX_TIMESTAMP(time) AS `time`,
            humidity,
            temperature
        FROM Air_Status air_s
        WHERE air_s.field_id = {form.field_id}
        ORDER BY time DESC
        LIMIT {form.limit};
        """
    )
    res = []
    for data in sql_data:
        res.append(
            FieldAirInfo(
                field_id=data[0],
                time=data[1],
                humidity=data[2],
                temperature=data[3]
            ).model_dump()
        )
    return ResponseModel(
        status="Success",
        msg="查询成功",
        data=res
    )


@router.post("/headwaters_info", summary="查询各农田水源质量传感器数据")
async def _():
    sql_data = execute_sql(
        """
        SELECT 
            field_id,
            time,
            ph,
            hardness,
            solids,
            chloramines,
            sulfate,
            conductivity,
            organic_carbon,
            trihalomethanes,
            turbidity,
            potability
        FROM (
            SELECT
                f.field_id AS `field_id`,
                UNIX_TIMESTAMP(hw_s.time) AS `time`,
                hw_s.ph AS `ph`,
                hw_s.hardness AS `hardness`,
                hw_s.solids AS `solids`,
                hw_s.chloramines AS `chloramines`,
                hw_s.sulfate AS `sulfate`,
                hw_s.conductivity AS `conductivity`,
                hw_s.organic_carbon AS `organic_carbon`,
                hw_s.trihalomethanes AS `trihalomethanes`,
                hw_s.turbidity AS `turbidity`,
                hw_s.potability AS `potability`,
                RANK() OVER (PARTITION BY f.field_id ORDER BY hw_s.time DESC) AS `rank`
            FROM Fields f LEFT JOIN Headwaters_Status hw_s ON (f.field_id = hw_s.field_id)
            ) tmp
        WHERE tmp.rank = 1;
        """
    )
    res = []
    for data in sql_data:
        res.append(
            FieldHeadwatersInfo(
                field_id=data[0],
                time=data[1],
                ph=data[2],
                hardness=data[3],
                solids=data[4],
                chloramines=data[5],
                sulfate=data[6],
                conductivity=data[7],
                organic_carbon=data[8],
                trihalomethanes=data[9],
                turbidity=data[10],
                potability=data[11],
            ).model_dump()
        )
    return ResponseModel(
        status="Success",
        msg="查询成功",
        data=res
    )


@router.post("/headwaters_info_single", summary="查询单个农田的最新水源质量传感器数据")
async def _(form: FieldSingleForm):
    count_data = execute_sql(
        f"""
        SELECT COUNT(*)
        FROM Fields f
        WHERE f.field_id = {form.field_id};
        """
    )
    if count_data[0][0] == 0:
        return ResponseModel(
            status="Fail",
            msg="所查询的农田不存在"
        )
    sql_data = execute_sql(
        f"""
        SELECT
            field_id,
            UNIX_TIMESTAMP(time) AS `time`,
            ph,
            hardness,
            solids,
            chloramines,
            sulfate,
            conductivity,
            organic_carbon,
            trihalomethanes,
            turbidity,
            potability
        FROM Headwaters_Status hw_s
        WHERE hw_s.field_id = {form.field_id}
        ORDER BY time DESC
        LIMIT {form.limit};
        """
    )
    res = []
    for data in sql_data:
        res.append(
            FieldHeadwatersInfo(
                field_id=data[0],
                time=data[1],
                ph=data[2],
                hardness=data[3],
                solids=data[4],
                chloramines=data[5],
                sulfate=data[6],
                conductivity=data[7],
                organic_carbon=data[8],
                trihalomethanes=data[9],
                turbidity=data[10],
                potability=data[11],
            ).model_dump()
        )
    return ResponseModel(
        status="Success",
        msg="查询成功",
        data=res
    )