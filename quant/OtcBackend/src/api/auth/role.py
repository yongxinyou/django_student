import math

from quant.utils import logger, validators
from quant.utils.exceptions import ValidationError
from quant.utils.http.web import routes, WebViewBase

from datas.role import role_data


@routes.view(r'/api/auth/role/')
class Role(WebViewBase):

    async def get(self):
        page = validators.int_field(self.query_params.get('page', 1))
        page_size = validators.int_field(self.query_params.get('page_size', 10))

        page_cursor = page_size * (page - 1)
        total_count, datas = await role_data.get_roles_by_page(page_cursor, page_size)
        cur_page = page
        cur_page_size = len(datas)
        if page_cursor + cur_page_size < total_count:
            next_page = cur_page + 1
        else:
            next_page = 1
        total_page = max(int(math.ceil(float(total_count) / page_size)), 1)
        for data in datas:
            del data['update_time']
        result = {
            'cur_page': cur_page,
            'next_page': next_page,
            'total_page': total_page,
            'roles': datas
        }
        return self.success(result)

    async def post(self):
        body = await self.request.json()
        logger.info('body:', body, caller=self)
        name = validators.string_field(body, 'name')
        describe = validators.string_field(body, 'description')
        page_id = validators.list_field(body, 'page_id')
        account_id = validators.list_field(body, 'account_id')
        bank_id = validators.list_field(body, 'bank_id')
        data = await role_data.get_role_by_role_name(name)
        if data:
            return self.error(data='角色名已存在')
        role_id = await role_data.create_new_role(name, describe, page_id, account_id, bank_id)
        result = {
            'role_id': role_id
        }
        return self.success(result, '创建成功')


@routes.view(r'/api/auth/role/{role_id:([0-9a-z]{24})}/')
class Role(WebViewBase):
    """角色管理
    """

    async def get(self):
        role_id = self.request.match_info['role_id']
        logger.debug('role_id:', role_id, caller=self)
        role_info = await role_data.get_role_by_role_id(role_id)
        result = {
            'role_id': role_info['_id'],
            'name': role_info['name'],
            'description': role_info['description'],
            'page_id': role_info['page_id'],
            'account_id': role_info['account_id'],
            'bank_id': role_info['bank_id'],
            'create_time': role_info['create_time']
        }
        return self.success(result)

    async def patch(self):
        role_id = self.request.match_info['role_id']
        body = await self.request.json()
        logger.debug('role_id:', role_id, 'body:', body, caller=self)
        name = validators.string_field(body, 'name')
        describe = validators.string_field(body, 'description')
        page_id = validators.list_field(body, 'page_id')
        account_id = validators.list_field(body, 'account_id')
        bank_id = validators.list_field(body, 'bank_id')

        update_fields = {}
        if name:
            update_fields['name'] = name
        if describe:
            update_fields['description'] = describe
        if page_id:
            update_fields['page_id'] = page_id
        if account_id:
            update_fields['account_id'] = account_id
        if bank_id:
            update_fields['bank_id'] = bank_id
        if not update_fields:
            raise ValidationError(msg='请填写需要修改的字段')
        await role_data.update_role(role_id, update_fields)
        return self.success({'role_id': role_id}, '修改成功')

    async def delete(self):
        """软删除，返回成功了，但是数据库还有数据"""
        role_id = self.request.match_info['role_id']
        logger.debug('role_id:', role_id, caller=self)
        await role_data.delete_role(role_id)
        return self.success({'role_id:': role_id}, '删除成功')