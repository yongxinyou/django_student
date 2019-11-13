"""
    用户控住
"""
import math

from quant.utils import logger, validators
from quant.utils.exceptions import ValidationError
from quant.utils.http.web import routes, WebViewBase

from datas.user_data import user_data


@routes.view(r'/api/auth/user/')
class User(WebViewBase):

    async def get(self):
        page = validators.int_field(self.query_params.get('page', 1))
        page_size = validators.int_field(self.query_params.get('page_size', 10))

        page_cursor = page_size * (page - 1)
        total_count, datas = await user_data.get_user_by_page(page_cursor, page_size)

        cur_page = page
        cur_page_size = len(datas)
        if page_cursor + cur_page_size < total_count:
            next_page = cur_page + 1
        else:
            next_page = 1
        total_page = max(int(math.ceil(float(total_count) / page_size)), 1)
        for data in datas:
            del data['_id']
            del data['create_time']
            del data['update_time']
        result = {
            'cur_page': cur_page,
            'next_page': next_page,
            'total_page': total_page,
            'users': datas
        }
        return self.success(result, '查找成功')

    async def post(self):
        body = await self.request.json()
        logger.info('body:', body, caller=self)
        username = validators.string_field(body, 'username')
        password = validators.string_field(body, 'password')
        verification = validators.string_field(body, 'verification')
        role_id = validators.string_field(body, 'role_id')
        data = await user_data.get_user_by_username(username)
        if data:
            return self.error(data='用户名已存在')
        user_id = await user_data.create_new_user(username, password, verification, role_id)
        result = {'user_id': user_id}
        return self.success(result, '创建成功')


@routes.view(r'/api/auth/user/{user_id:([0-9a-z]{24})}/')
class User(WebViewBase):
    """
    用户管理
    """

    async def get(self):
        user_id = self.request.match_info['user_id']
        logger.debug('user_id:', user_id, caller=self)
        user_info = await user_data.get_user_by_user_id(user_id)
        result = {
            'username': user_info['username'],
            'password': user_info['password'],
            'verification': user_info['verification'],
            'role_id': user_info['role_id']
        }
        return self.success(result, '查找成功')

    async def patch(self):
        user_id = self.request.match_info['user_id']
        body = await self.request.json()
        logger.debug('user_id:', user_id, 'body:', body, caller=self)
        username = validators.string_field(body, 'username', False)
        password = validators.string_field(body, 'password', False)
        verification = validators.string_field(body, 'verification', False)
        role_id = validators.string_field(body, 'role_id', False)

        update_fields = {}
        if username:
            update_fields['username'] = username
        if password:
            update_fields['password'] = password
        if verification:
            update_fields['verification'] = verification
        if role_id:
            update_fields['role_id'] = role_id
        if not update_fields:
            raise ValidationError(msg='请填写需要修改的字段')
        await user_data.update_user(user_id, update_fields)
        return self.success({'user_id': user_id}, '修改成功')

    async def delete(self):
        user_id = self.request.match_info['user_id']
        logger.debug('user_id:', user_id, caller=self)
        await user_data.delete_user(user_id)
        return self.success({'user_id': user_id}, '删除成功')