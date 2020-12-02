from apps import db
from orm.model import User
from utils import MD5Util
from flask import Blueprint, request, make_response, jsonify, current_app, app
from sqlalchemy import or_, and_
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import session, Response
from sqlalchemy.sql import exists
import datetime

# 创建一个蓝图，蓝图名称 user，前缀 /user
user_dp = Blueprint("user", __name__, url_prefix="/user")


# 后面写API接口 =============================================================
@user_dp.after_request
def af_req(resp):  # 解决跨域session丢失
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    resp.headers['Access-Control-Allow-Methods'] = 'PUT,POST,GET,DELETE,OPTIONS'
    # resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Content-Length, Authorization, Accept, ' \
                                                   'X-Requested-With , yourHeaderFeild '
    resp.headers['Access-Control-Allow-Credentials'] = 'true'

    resp.headers['X-Powered-By'] = '3.2.1'
    resp.headers['Content-Type'] = 'application/json;charset=utf-8'
    return resp


def create_token(uid, scope=None, expiration=5000):
    # 通过flask提供的对象，传入过期时间和flask的SECRET_KEY
    """生成令牌"""
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    # token里面的值，是技术方案需要订的，做相关的业务逻辑验证，uid唯一值表示当前请求的客户端
    # type表示客户端类型，看业务场景进行增删
    # scope权限作用域
    # 设置过期时间，这个是必须的，一般设置两个小时
    return s.dumps({
        'uid': uid,
        # 'type': type.value,
        'scope': scope
    }).decode('ascii')


# 登录判断
@user_dp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # 获取用户名和密码，并密码加密
        username = request.json['username']
        password = request.json['password']
        password = MD5Util.md5vale(password)

        # 将用户名和加密后的密码去数据库查询
        user = db.session.query(User).filter(and_(
            User.loginName == username,
            User.password == password
        )).first()
        # 查询角色
        print(user)

        result = {}
        data = {}
        if user is not None:  # 登录成功
            result["flag"] = True
            result["msg"] = "登录成功"
            data["token"] = create_token(user.id)

            # result["data"] = user.to_json()
            result["data"] = data
            result["code"] = 1
        else:  # 登录失败
            result["flag"] = False
            result["msg"] = "登录失败123"

        print(result["msg"])

        # 解决前后端分离跨域问题
        rst = make_response(jsonify(result))
        # rst.headers['Access-Control-Allow-Origin'] = '*'  # 任意域名
        # if request.method == 'POST':
        #     rst.headers['Access-Control-Allow-Methods'] = 'POST'  # 响应POST
        return rst


def verify_token(token):
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        # 转换为字典
        user_id = s.loads(token)

    except Exception:
        return None
    return user_id


@user_dp.route('/info')
def info():
    token = request.headers["Authorization"]
    user_id = verify_token(token)
    if user_id:
        print(user_id["uid"])

        data = {
            "avatar": "https://randy168.com/1533262153771.gif",
            "roles": ["admin", ],
            "data": ["order-manage", "order-list", "product-manage", "product-list", "review-manage", "return-goods",
                     "goods", "goods-list", "goods-classify", "permission", "user-manage", "role-manage", "menu-manage"]
        }
        return {
            "code": 1,
            "data": data
        }
    else:
        return "登录失败"


# 获取用户列表
@user_dp.route('/list', methods=["GET"])
def get():
    """
    从数据库中获取数据
    """
    # todo 分页查询，按姓名模糊查询
    # 多表操作 使用原生sql查询
    user_list = db.session.execute(
        "SELECT u.*,r.id as rid, r.displayName FROM tab_user_role ur right join tab_user u on ur.user_id=u.id left join tab_role r on ur.role_id=r.id")

    # user_list = User.query.all()
    user_list_dict = []
    for user in user_list:
        user_list_dict.append(
            {
                'id': user.id,
                'loginName': user.loginName,
                'address': user.address,
                'email': user.email,
                'status': user.status,
                'realName': user.realName,
                'mobile': user.mobile,
                'lastLoginTime': user.lastLoginTime,
                "erpMemberRoles": [{
                    "id": user.rid or "Null",
                    "roleName": user.displayName or "未分配权限"
                }]
            }
        )

    return {
        "code": 1,
        "data": user_list_dict
    }


# 重置密码
@user_dp.route('/reset', methods=["POST"])
def resetPwd():
    uid = request.json['id']
    print(uid)
    # todo 可以先查询密码是否已经是初始密码
    res = db.session.query(User).filter(User.id == uid).update({"password": "e10adc3949ba59abbe56e057f20f883e"})
    db.session.commit()
    db.session.close()
    if res:
        return {
            "code": 1,
            "msg": "初始化完成"
        }
    else:
        return {
            "code": 0,
            "msg": "请稍后重试"
        }


# 创建用户
@user_dp.route('/create', methods=["POST"])
def createUser():
    '''
    创建用户的接口
    :return:
    '''

    # 获取数据
    data = request.json["data"]
    print(data)
    # 判断登录名是否存在
    obj = db.session.query(exists().where(User.loginName == data['loginName'])).scalar()
    if obj:
        return{
            "code": 0,
            "msg": "登录名已存在"
        }
    else:
        user = User(
            loginName=data['loginName'],
            password="e10adc3949ba59abbe56e057f20f883e",
            realName=data['realName'],
            mobile=data['mobile'],
            address=data['address'],
            email=data['email'],
            lastLoginTime=datetime.datetime.now(),
            status=1,  # 默认启用
        )

        for rid in data["tempRoleIds"]:
            user.role.append(rid)
        db.session.add(user)
        db.session.flush()
        # db.session.commit()
        # 输出新插入数据的主键
        print(user.id)
        print(data["tempRoleIds"][0])

        # urole=tab_user_role(tab_user_role.userid=user.id,data["tempRoleIds"])
        # print(urole)
        return {
            "code": 1,
            "msg": "创建成功,初始密码:123456"
        }