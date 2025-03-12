from .db import execute_sql
from models.response_models import ResponseModel

def check_user_exists(user_id: int) -> bool:
    """检查用户是否存在"""
    sql_data = execute_sql(
        f"""
        SELECT COUNT(*)
        FROM Users
        WHERE Users.user_id = {user_id};
        """
    )
    if sql_data[0][0] == 0:
        return False
    else:
        return True

def permission_test(user_name,target_user_name,profile_data):
    data = execute_sql(
        f"SELECT COUNT(*) FROM Users WHERE user_name='{user_name}';")
    if data[0][0] == 0:
        return ResponseModel(status="Fail", msg="用户不存在", data=dict(profile_data))
    data = execute_sql(
        f"SELECT COUNT(*) FROM Users WHERE user_name='{target_user_name}';")
    if data[0][0] == 0:
        return ResponseModel(status="Fail", msg="目标用户不存在", data=dict(profile_data))
    data = execute_sql(
        f"SELECT is_admin FROM Users WHERE user_name='{user_name}';")
    if data[0][0] == 0 and user_name != target_user_name:
        return ResponseModel(status="Fail", msg="你没有权限", data=dict(profile_data))
    return ResponseModel(status="Success", msg="校验成功", data=dict(profile_data))

def delete_permission(user_name,target_user_name,return_data):
    data = execute_sql(
        f"SELECT COUNT(*) FROM Users WHERE user_name='{user_name}';")
    if data[0][0] == 0:
        return ResponseModel(status="Fail", msg="用户不存在", data=return_data)
    data = execute_sql(
        f"SELECT COUNT(*) FROM Users WHERE user_name='{target_user_name}';")
    if data[0][0] == 0:
        return ResponseModel(status="Fail", msg="目标用户不存在", data=return_data)
    data = execute_sql(
        f"SELECT is_admin FROM Users WHERE user_name='{user_name}';")
    if data[0][0] == 0 and user_name != target_user_name:
        return ResponseModel(status="Fail", msg="没有权限", data=return_data)
    return ResponseModel(status="Success", msg="校验成功", data=return_data)

def generate_query(condition,limit = 50):
    user_id = condition.user_id
    field_id = condition.field_id
    start_date = condition.start_date
    end_date = condition.end_date
    fertilizer_type = condition.type
    min_density = condition.min_density
    max_density = condition.max_density
    query = "SELECT * FROM Fertilization WHERE "
    conditions = []
    if user_id is not None:
        conditions.append(f"user_id = {user_id}")
    if field_id is not None:
        conditions.append(f"field_id = {field_id}")
    if start_date is not None:
        conditions.append(f"date >= '{start_date}'")
    if end_date is not None:
        conditions.append(f"date <= '{end_date}'")
    if min_density is not None:
        conditions.append(f"density >= {min_density}")
    if max_density is not None:
        conditions.append(f"density <= {max_density}")
    if fertilizer_type is not None:
        conditions.append(f"type = '{fertilizer_type}'")
    if conditions:
        query += " AND ".join(conditions)
    else:
        return f"SELECT * FROM Fertilization ORDER BY date DESC LIMIT {limit}"
    query += f" ORDER BY date DESC LIMIT {limit}"
    return query

def is_admin_test(user_name):
    data = execute_sql(
        f"SELECT COUNT(*) FROM Users WHERE user_name='{user_name}';")
    if data[0][0] == 0:
        return ResponseModel(status="Fail", msg="用户不存在", data=dict(user_name=user_name))
    data = execute_sql(
        f"SELECT is_admin FROM Users WHERE user_name='{user_name}';")
    if data[0][0] == 0:
        return ResponseModel(status="Fail", msg="没有权限", data=dict(user_name=user_name))
    return ResponseModel(status="Success", msg="校验成功", data=dict(user_name=user_name))

def check_user_admin(user_id: int) -> bool:
    """检查用户是否为管理员"""
    sql_data = execute_sql(
        f"""
        SELECT COUNT(*)
        FROM Users
        WHERE
            `user_id` = {user_id}
            AND `is_admin` = 1;
        """
    )
    if sql_data[0][0] == 0:
        return False
    else:
        return True

def is_chinese(text):
    for c in text:
        """判断一个unicode是否是汉字"""
        if c >= u'\u4e00' and c <= u'\u9fa5':
            return True
    return False

def calculate_byte_length(string):
    byte_length = len(string.encode('utf-8'))
    return byte_length


