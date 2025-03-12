from fastapi import APIRouter

from utils import execute_sql, logger, permission_test, delete_permission, is_admin_test,is_chinese,calculate_byte_length
from models.response_models import ResponseModel
from models.user_models import (
    UserLoginModel,
    UserRegisterModel,
    UserProfileModel,
    UserProfileEditModel,
    UserProfileResponseModel,
    UserDeleteModel,
    UserNameModel
)


router = APIRouter()

@router.post("/login")
async def _(login_data: UserLoginModel):
    logger.debug(login_data.model_dump())
    data = execute_sql(f"SELECT COUNT(*) FROM Users WHERE user_name='{login_data.user_name}' and is_admin = {login_data.is_admin} and available = 1;")
    try:
        if data[0][0] == 0:
            #用户不存在
            return ResponseModel(status="Fail", msg="用户不存在，登录失败。",data = dict(login_data))
        data = execute_sql(f"SELECT COUNT(*) FROM Users WHERE user_name='{login_data.user_name}' and password = '{login_data.password}' and is_admin = {login_data.is_admin};")
        if data[0][0] == 0:
            #密码错误
            return ResponseModel(status="Fail", msg="密码错误。",data = dict(login_data))
        #data = execute_sql(
        #    f"SELECT * FROM users WHERE user_name='{login_data.user_name}' and password = '{login_data.password}' and is_admin = '{login_data.is_admin}';")
        return ResponseModel(status="Success", msg="登录成功",data = dict(login_data))
    except Exception as e:
        return ResponseModel(status="Fail", msg="数据库执行未知错误",data = dict(login_data))

@router.post("/register")
async def _(register_data: UserRegisterModel):
    logger.debug(register_data.model_dump())
    data = execute_sql(f"SELECT COUNT(*) FROM Users WHERE user_name='{register_data.user_name}';")
    if is_chinese(register_data.user_name):
        return ResponseModel(status="Fail", msg="用户名不可为中文", data=dict(register_data))
    if calculate_byte_length(register_data.user_name) < 3:
        return ResponseModel(status="Fail", msg="用户名不可为少于3个字符", data=dict(register_data))
    if is_chinese(register_data.password):
        return ResponseModel(status="Fail", msg="密码不可为中文", data=dict(register_data))
    if len(register_data.user_name) > 10:
        return ResponseModel(status="Fail", msg="用户名不可超过10位", data=dict(register_data))
    if len(register_data.password) > 32:
        return ResponseModel(status="Fail", msg="密码过长", data=dict(register_data))
    if len(register_data.password) < 3:
        return ResponseModel(status="Fail", msg="密码不得小于3个字符", data=dict(register_data))
    if data[0][0] != 0:
        return ResponseModel(status="Fail", msg="用户已存在，注册失败。",data = dict(register_data))
    try:
        if calculate_byte_length(register_data.user_form.name) > 20:
            return ResponseModel(status="Fail", msg="昵称不可过长", data=dict(register_data))
        if calculate_byte_length(register_data.user_form.note) > 100:
            return ResponseModel(status="Fail", msg="备注不可过长", data=dict(register_data))
        sql = f"INSERT INTO Users(is_admin,user_name,password,name,note) VALUES \
                       ({register_data.user_form.is_admin}, '{register_data.user_name}', '{register_data.password}', '{register_data.user_form.name}', '{register_data.user_form.note}');"
        execute_sql(sql)
    except Exception as e:
        return ResponseModel(status="Fail", msg="数据库执行未知错误",data = dict(register_data))
    return ResponseModel(status="Success", msg="注册成功",data = dict(register_data))


# 查询用户信息接口
@router.post("/info")
async def get_profile(profile_data: UserProfileModel):
    # 实现查询用户信息逻辑
    # 查询逻辑包括根据用户名查询用户信息等
    logger.debug(profile_data.model_dump())
    try:
        responseModel = permission_test(profile_data.user_name,profile_data.target_user_name,profile_data)
        if responseModel.status == "Fail":
            return responseModel
        else:
            data = execute_sql(
                f"SELECT * FROM Users WHERE user_name='{profile_data.target_user_name}';")
            resData = dict(UserProfileResponseModel(user_id = data[0][0],is_admin = data[0][1] == 1,user_name = data[0][2],name = data[0][4],note = data[0][5]))
            return ResponseModel(status="Success", msg="查询成功", data=resData)
    except:
        return ResponseModel(status="Fail", msg="数据库执行未知错误", data=profile_data.model_dump())

# 更改用户信息接口
@router.post("/update")
async def edit_profile(profile_data: UserProfileEditModel):
    logger.debug(profile_data.model_dump())
    try:
        responseModel = permission_test(profile_data.user_name,profile_data.target_user_name,profile_data)
        if responseModel.status == "Fail":
            return responseModel
        else:
            if is_chinese(profile_data.user_form.password):
                return ResponseModel(status="Fail", msg="密码不可以为中文", data=dict(profile_data))
            if len(profile_data.user_form.password) > 32:
                return ResponseModel(status="Fail", msg="密码过长", data=dict(profile_data))
            if len(profile_data.user_form.password) < 3:
                return ResponseModel(status="Fail", msg="密码不得小于3个字符", data=dict(profile_data))
            if calculate_byte_length(profile_data.user_form.name) > 20:
                return ResponseModel(status="Fail", msg="昵称不可过长", data=dict(profile_data))
            if calculate_byte_length(profile_data.user_form.note) > 100:
                return ResponseModel(status="Fail", msg="备注不可过长", data=dict(profile_data))
            sql = (f"UPDATE Users SET \
                   name='{profile_data.user_form.name}', password='{profile_data.user_form.password}', note='{profile_data.user_form.note}'\
                   WHERE user_name='{profile_data.target_user_name}';")
            execute_sql(sql)
            data = execute_sql(
                f"SELECT * FROM Users WHERE user_name='{profile_data.target_user_name}';")
            resData = dict(UserProfileResponseModel(user_id = data[0][0],is_admin = data[0][1] == 1,user_name = data[0][2],name = data[0][4],note = data[0][5]))
            return ResponseModel(status="Success", msg="修改成功", data=resData)
    except:
        return ResponseModel(status="Fail", msg="数据库执行未知错误", data=dict(profile_data))

@router.post("/delete")
async def _(profile_data: UserDeleteModel):
    logger.debug(profile_data.model_dump())
    try:
        res = delete_permission(profile_data.user_name,profile_data.target_user_name,dict(profile_data))
        if res.status == "Fail":
            return res
        #execute_sql(
        #        f"DELETE FROM Users WHERE user_name='{profile_data.target_user_name}';")
        #return f"UPDATE Users SET available = 0 WHERE user_name='{profile_data.target_user_name}';"
        execute_sql(
                f"UPDATE Users SET available = false WHERE user_name='{profile_data.target_user_name}';")

        return ResponseModel(status="Success", msg="删除成功", data=dict(profile_data))
    except:
        return ResponseModel(status="Fail", msg="数据库执行未知错误", data=dict(profile_data))


@router.post("/findall")
async def _(form: UserNameModel):
    logger.debug(form.model_dump())
    test = is_admin_test(form.user_name)
    if test.status == "Success":
        data = execute_sql(f"SELECT * FROM Users WHERE available = 1")
        allUsers = []
        for i in data:
            allUsers.append(dict(is_admin = i[1] == 1,user_name=i[2],name = i[4],note = i[5]))
        return ResponseModel(status="Success", msg="查询成功", data=allUsers)
    else:
        return test

@router.post("/findId")
async def _(form: UserNameModel):
    logger.debug(form.model_dump())
    test = is_admin_test(form.user_name)
    if test.status == "Success":
        data = execute_sql(f"SELECT * FROM Users")
        allUsers = []
        for i in data:
            allUsers.append(dict(is_admin = i[1] == 1,user_name=i[2],name = i[4],note = i[5]))
        return ResponseModel(status="Success", msg="查询成功", data=allUsers)
    else:
        return test