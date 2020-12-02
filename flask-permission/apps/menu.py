from flask import Blueprint, request, make_response, jsonify
from sqlalchemy import or_, and_
from apps import db
from orm.model import Menu

# 创建一个蓝图，蓝图名称 menu，前缀 /menu
menu_dp = Blueprint("menu", __name__, url_prefix="/menu")

# 后面写API接口 =============================================================
