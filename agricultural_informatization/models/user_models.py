from pydantic import BaseModel
from typing import Optional


class UserInfo(BaseModel):
    """用户的所有信息"""

    user_id: int
    """用户自增ID"""

    is_admin: bool
    """是否为管理员"""

    user_name: str
    """用户名，应只有英文与数字"""

    password: str
    """用户密码，用32位MD5加密"""

    name: str
    """用户昵称"""

    note: Optional[str] = None
    """备注信息"""

class UserForm(BaseModel):
    """用户本身可看到的所有信息"""

    is_admin: bool
    """是否为管理员"""

    user_name: str
    """用户名，应只有英文与数字"""

    password: str
    """用户密码，用32位MD5加密"""

    name: str
    """用户昵称"""

    note: Optional[str] = None
    """备注信息"""

class UserLoginModel(BaseModel):
    """用户登录数据"""

    is_admin: bool
    """是否为管理员"""

    user_name: str
    """用户名，应只有英文与数字"""

    password: str
    """用户密码，用32位MD5加密"""

class UserRegisterModel(BaseModel):
    """用户注册数据"""

    user_name: str
    """用户名，应只有英文与数字"""

    password: str
    """用户密码，用32位MD5加密"""

    user_form: UserForm
    """用户信息"""

class UserProfileModel(BaseModel):
    """用户查询数据"""

    user_name: str
    """请求来自的用户"""

    target_user_name: str
    """查询目标用户名"""

class UserProfileEditModel(BaseModel):
    """用户编辑数据"""

    user_name: str
    """请求来自的用户"""

    target_user_name: str
    """编辑目标用户名"""

    user_form: UserForm
    """需要修改的用户信息"""

class UserProfileResponseModel(BaseModel):
    """用户查询以后返回的数据"""
    user_id: int
    """是否为管理员"""

    is_admin: bool
    """是否为管理员"""

    user_name: str
    """用户名，应只有英文与数字"""

    name: str
    """用户昵称"""

    note: Optional[str] = None
    """备注信息"""

class UserDeleteModel(BaseModel):
    """用户删除数据"""

    user_name: str
    """请求来自的用户"""

    target_user_name: str
    """编辑目标用户名"""

class UserNameModel(BaseModel):
    """用户名"""

    user_name: str
    """用户名，应只有英文与数字"""