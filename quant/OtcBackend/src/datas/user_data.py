# -*- coding:utf-8 -*-

"""
    user 数据存储接口
"""

from quant.db.mongo import MongoDBBase


__all__ = ('user_data', )


class UserData(MongoDBBase):
    """ 用户账户数据
    """

    async def create_new_user(self, username, password, verification, role):
        """ 创建新用户
        """
        data = {
            'username': username,
            'password': password,
            'verification': verification,
            'role_id': role,
        }
        user_id = await self.insert(data)
        return user_id

    async def get_user_by_page(self, page_cursor=0, page_size=9999):
        """ 分页查询数据
        @param page_cursor 当前游标位置
        @param page_size 请求数据条数
        """
        sort = [
            ('create_time', -1)
        ]
        datas = await self.get_list(sort=sort, skip=page_cursor, limit=page_size)
        total_datas = await self.get_list(sort=sort)
        count = len(total_datas)
        return count, datas

    async def get_user_by_username(self, username):
        """ 根据用户昵称查询用户
        """
        spec = {
            'username': username
        }
        data = await self.find_one(spec)
        return data

    async def get_user_by_user_id(self, user_id):
        """ 根据用户昵称id用户
        """
        spec = {
            '_id': user_id
        }
        data = await self.find_one(spec)
        return data

    async def get_user_by_role(self, role):
        """
        根据角色查询用户
        :param role:
        :return:
        """
        spec = {
            'role': role
        }
        fields = {
            'username': 1,
            'verification': 1,
            'role': 1,
        }
        data = await self.get_list(spec, fields)
        return data

    async def update_user(self, user_id, update_fields):
        """
        修改用户配置
        :param verification:
        :param role:
        :return:
        """
        spec = {
            '_id': user_id
        }
        await self.update(spec, {'$set': update_fields})

    async def delete_user(self, user_id):
        """
        删除用户
        :param user_id:
        :return:
        """
        spec = {
            '_id': user_id
        }
        await self.delete(spec)


user_data = UserData('otc', 'user')
