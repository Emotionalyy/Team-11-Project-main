from fastapi import APIRouter

from models.agri_mach_models import (
    AgriMachInfo,
    AddAgriMachUseForm
)
from models.response_models import ResponseModel
from utils import execute_sql, check_user_exists


router = APIRouter()


@router.post("/list", summary="展示所有农机")
async def _():
    sql_data = execute_sql(
        """
        WITH 
        agri_mach_last_used_tmp AS (
            SELECT
                tmp.mach_id AS `mach_id`,
                tmp.date AS `last_used_date`
            FROM (
                SELECT
                    am.mach_id AS `mach_id`,
                    am_use.date AS `date`,
                    RANK() OVER (PARTITION BY `mach_id` ORDER BY `date` DESC) as `rank`
                FROM Agri_Mach am LEFT JOIN Agri_Mach_Use am_use ON (am.mach_id = am_use.mach_id)
            ) tmp
            WHERE tmp.rank = 1
        ),
        agri_mach_last_main_tmp AS (
            SELECT
                tmp.mach_id AS `mach_id`,
                tmp.date AS `last_main_date`
            FROM (
                SELECT
                    am.mach_id AS `mach_id`,
                    am_main.date AS `date`,
                    RANK() OVER (PARTITION BY `mach_id` ORDER BY `date` DESC) as `rank`
                FROM Agri_Mach am LEFT JOIN (
                    SELECT
                        Agri_Mach_Use.mach_id AS `mach_id`,
                        Agri_Mach_Use.date AS `date`
                    FROM Agri_Mach_Use WHERE main_status
                ) am_main ON (am.mach_id = am_main.mach_id)
            ) tmp
        )
        SELECT
            am.mach_id as `mach_id`,
            am.name as `name`,
            am.usage as `usage`,
            am.mach_status as `mach_status`,
            am_main_tmp.last_main_date as `last_main_date`,
            am_used_tmp.last_used_date as `last_used_date`
        FROM Agri_Mach am
            JOIN agri_mach_last_used_tmp am_used_tmp ON (am.mach_id = am_used_tmp.mach_id)
            JOIN agri_mach_last_main_tmp am_main_tmp ON (am.mach_id = am_main_tmp.mach_id);
        """
    )
    res = []
    for data in sql_data:
        res.append(
            AgriMachInfo(
                mach_id=data[0],
                name=data[1],
                usage=data[2],
                mach_status=data[3],
                last_main_date=data[4],
                last_used_date=data[5]
            ).model_dump()
        )
    return ResponseModel(
        status="Success",
        msg="查询成功",
        data=res
    )

@router.post("/add_use", summary="添加农机使用数据")
async def _(form: AddAgriMachUseForm):
    if not check_user_exists(form.user_id):
        return ResponseModel(
            status="Fail",
            msg="发送请求的用户不存在。"
        )
    if not check_user_exists(form.data.user_id):
        return ResponseModel(
            status="Fail",
            msg="施肥操作用户不存在。"
        )
    count_data = execute_sql(
        f"""
        SELECT COUNT(*)
        FROM Agri_Mach
        WHERE Agri_Mach.mach_id = {form.data.mach_id};
        """
    )
    if count_data[0][0] == 0:
        return ResponseModel(
            status="Fail",
            msg="事件中的农机不存在。"
        )
    execute_sql(
        f"""
        INSERT INTO Agri_Mach_Use
        VALUES (
            0,
            {form.data.mach_id},
            {form.data.user_id},
            '{form.data.date}',
            '{form.data.note}',
            {1 if form.data.main_status else 0}
        );
        """
    )
    return ResponseModel(
        status="Success",
        msg="添加成功"
    )

@router.post("/need_main", summary="查询所有需要维护的农机，30天以上")
async def _():
    sql_data = execute_sql(
        """
        WITH 
        agri_mach_last_used_tmp AS (
            SELECT
                tmp.mach_id AS `mach_id`,
                tmp.date AS `last_used_date`
            FROM (
                SELECT
                    am.mach_id AS `mach_id`,
                    am_use.date AS `date`,
                    RANK() OVER (PARTITION BY `mach_id` ORDER BY `date` DESC) as `rank`
                FROM Agri_Mach am LEFT JOIN Agri_Mach_Use am_use ON (am.mach_id = am_use.mach_id)
            ) tmp
            WHERE tmp.rank = 1
        ),
        agri_mach_last_main_tmp AS (
            SELECT
                tmp.mach_id AS `mach_id`,
                tmp.date AS `last_main_date`
            FROM (
                SELECT
                    am.mach_id AS `mach_id`,
                    am_main.date AS `date`,
                    RANK() OVER (PARTITION BY `mach_id` ORDER BY `date` DESC) as `rank`
                FROM Agri_Mach am LEFT JOIN (
                    SELECT
                        Agri_Mach_Use.mach_id AS `mach_id`,
                        Agri_Mach_Use.date AS `date`
                    FROM Agri_Mach_Use WHERE main_status
                ) am_main ON (am.mach_id = am_main.mach_id)
            ) tmp
        )
        SELECT
            am.mach_id as `mach_id`,
            am.name as `name`,
            am.usage as `usage`,
            am.mach_status as `mach_status`,
            am_main_tmp.last_main_date as `last_main_date`,
            am_used_tmp.last_used_date as `last_used_date`
        FROM Agri_Mach am
            JOIN agri_mach_last_used_tmp am_used_tmp ON (am.mach_id = am_used_tmp.mach_id)
            JOIN agri_mach_last_main_tmp am_main_tmp ON (am.mach_id = am_main_tmp.mach_id)
        WHERE
            am_main_tmp.last_main_date IS NULL OR DATEDIFF(CURRENT_DATE(), am_main_tmp.last_main_date) > 30;
        """
    )
    res = []
    for data in sql_data:
        res.append(
            AgriMachInfo(
                mach_id=data[0],
                name=data[1],
                usage=data[2],
                mach_status=data[3],
                last_main_date=data[4],
                last_used_date=data[5]
            ).model_dump()
        )
    return ResponseModel(
        status="Success",
        msg="查询成功",
        data=res
    )

