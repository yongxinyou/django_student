"""
    用户角色数据
"""

from quant.db.mongo import MongoDBBase

__all__ = ('role_data', )


class RoleData(MongoDBBase):
    """
    用户角色表
    """

    async def create_new_role(self, name, description, page_id, account_id, bank_id):
        """
        创建新角色
        """
        data = {
            'name': name,                    # 名称
            'description': description,      # 描述信息
            'page_id': page_id,              # 可用页面id
            'account_id': account_id,        # 可用账号id
            'bank_id': bank_id,              # 可用银行卡id
        }
        user_id = await self.insert(data)
        return user_id

    async def get_roles_by_page(self, page_cursor=0, page_size=9999):
        """
        分页查询数据
        :param page_cursor: 当前游标位置
        :param page_size:  请求数据条数
        """
        sort = [
            ('create_time', -1)
        ]
        datas = await self.get_list(sort=sort, skip=page_cursor, limit=page_size)
        total_datas = await self.get_list(sort=sort)
        count = len(total_datas)
        return count, datas

    async def get_role_by_role_id(self, role_id):
        """
        根据角色id查询角色
        """
        spec = {
            '_id': role_id
        }
        data = await self.find_one(spec)
        return data

    async def get_role_by_role_name(self, role_name):
        """
        根据角色名称查询角色
        :param role_name:
        :return:
        """
        spec = {
            'name': role_name
        }
        data = await self.find_one(spec)
        return data

    async def update_role(self, role_id, update_fields):
        """更新角色配置
        """
        spec = {
            '_id': role_id
        }
        await self.update(spec, {'$set': update_fields})

    async def delete_role(self, role_id):
        """删除角色配置
        """
        spec = {
            '_id': role_id
        }
        await self.delete(spec)


role_data = RoleData('otc', 'role')