from datetime import timedelta
from fastapi import APIRouter,FastAPI

from models.field_models import AddFertilizationForm,SearchFertilizationForm,FertilizationInfo
from models.response_models import ResponseModel
from utils import execute_sql, check_user_exists
from utils.user import *

app = FastAPI()
router = APIRouter()

@router.post("/add", summary="添加施肥事件")
async def _(form: AddFertilizationForm):
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
    execute_sql(
        f"""
        INSERT INTO Fertilization
        VALUES(
            0,
            {form.data.user_id},
            {form.data.field_id},
            '{form.data.date}',
            '{form.data.type}',
            {form.data.density},
            '{form.data.note}'
        )
        """
    )
    return ResponseModel(
        status="Success",
        msg="添加成功",
        data={
            "next_time": form.data.date + timedelta(30)
        }
    )

@router.post("/search", summary="条件搜索施肥事件")
async def _(form: SearchFertilizationForm):
    #form.user_id
    mysql_query = generate_query(form.search_condition,form.number_limit)
    #return mysql_query
    data = execute_sql(mysql_query)
    all_items = []
    for onedata in data:
        i = dict(FertilizationInfo(user_id = onedata[1],
                          field_id = onedata[2],
                          date = onedata[3],
                          type = onedata[4],
                          density = onedata[5],
                          note = onedata[6]))
        all_items.append(i)
    return ResponseModel(
        status="Success",
        msg="查询成功",
        data={
            "number": len(all_items),
            "all_items": all_items
        })

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
# 示例用法
