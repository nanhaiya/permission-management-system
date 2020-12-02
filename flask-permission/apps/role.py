from flask import Blueprint, request, make_response, jsonify
from sqlalchemy import or_, and_
from apps import db
from orm.model import Role

# 创建一个蓝图，蓝图名称 role，前缀 /role
role_dp = Blueprint("role", __name__, url_prefix="/role")

# 后面写API接口 =============================================================


# 查询所有角色接口，参数args参数 当前页、每页查询条数，如果条件查询，参数为json类型的条件参数
# 未做前后端跨域处理
@role_dp.route('/findAll', methods=['GET', 'POST'])
def find_all():
    currentPage = 1
    pageSize = 2
    pg = db.session.query(Role).paginate(currentPage, pageSize)
    roles = []
    for r in pg.items:
        roles.append(r.to_json())
    return jsonify({'data': roles, 'total': pg.total})
