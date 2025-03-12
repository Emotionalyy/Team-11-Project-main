from fastapi import HTTPException, Query
from typing import Callable

from .user import check_user_admin, check_user_exists
from models.response_models import ResponseModel


def permission_check(
        need_user_exist: bool = True,
        need_user_admin: bool = False
    ) -> Callable:
    """检查用户权限"""
    async def inner(user_id: int = Query(default=0)):
        nonlocal need_user_exist
        nonlocal need_user_admin
        if need_user_admin:
            need_user_exist = True
        if need_user_exist and not check_user_exists(user_id):
            # return ResponseModel(
            #     status="Fail",
            #     msg="该接口要求用户存在于数据库中，但未找到当前请求用户。"
            # )
            raise HTTPException(
                status_code=403,
                detail="该接口要求用户存在于数据库中，但未找到当前请求用户。"
            )
        if need_user_admin and not check_user_admin(user_id):
            # return ResponseModel(
            #     status="Fail",
            #     msg="该接口要求用户拥有管理员权限，但当前请求用户非管理员。"
            # )
            raise HTTPException(
                status_code=403,
                detail="该接口要求用户拥有管理员权限，但当前请求用户非管理员。"
            )
    return inner