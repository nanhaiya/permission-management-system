from apps import db


# 用户表
class User(db.Model):
    # 定义表名
    __tablename__ = 'tab_user'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 用户编号
    loginName = db.Column(db.String(32))  # 登录名
    password = db.Column(db.String(32))  # 密码
    realName = db.Column(db.String(32))  # 真实姓名
    mobile = db.Column(db.String(11))
    address = db.Column(db.String(255))
    email = db.Column(db.String(32))
    lastLoginTime = db.Column(db.Date)
    status = db.Column(db.Integer)
    role = db.relationship('Role', backref='user', secondary='tab_user_role')  # 关联角色表

    # 将数据转换成 json 格式
    def to_json(self):
        data_json = {
            "id": self.id,
            "loginName": self.loginName,
            "password": self.password,
            "realName": self.realName,
            "mobile": self.mobile,
            "address": self.address,
            "email": self.email,
            "lastLoginTime": self.lastLoginTime,
            "status": self.status
        }
        return data_json


# 角色表
class Role(db.Model):
    # 定义表名
    __tablename__ = 'tab_role'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 用户编号
    roleName = db.Column(db.String(32))  # 角色名
    displayName = db.Column(db.String(32))
    user_id = db.column(db.Integer, db.ForeignKey('tab_user.id'))  # 关联用户表
    permission = db.relationship('Permission', backref='permission', secondary='tab_role_permission')  # 关联权限表

    # 将数据转换成 json 格式
    def to_json(self):
        data_json = {
            "id": self.id,
            "name": self.name
        }
        return data_json


# class UserRole(db.Model):
#     __tablename__ = 'tab_user_role',
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 用户编号
#     user_id = db.Column(db.Integer, db.ForeignKey('tab_user.id')),
#     role_id = db.Column(db.Integer, db.ForeignKey('tab_role.id'))


# 用户和角色中间表
tab_user_role = db.Table(
    'tab_user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('tab_user.id')),  # 用户编号
    db.Column('role_id', db.Integer, db.ForeignKey('tab_role.id'))  # 角色编号
)


# 权限表
class Permission(db.Model):
    # 定义表名
    __tablename__ = 'tab_permission'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 用户编号
    name = db.Column(db.String(32))  # 权限名
    code = db.Column(db.String(32))  # 权限编码
    role_id = db.column(db.Integer, db.ForeignKey('tab_role.id'))  # 关联角色表
    menu = db.relationship('Menu', backref='menu', secondary='tab_permission_menu')  # 关联菜单表

    # 将数据转换成 json 格式
    def to_json(self):
        data_json = {
            "id": self.id,
            "name": self.name,
            "code": self.code
        }
        return data_json


# 角色和权限中间表
tab_user_role = db.Table(
    'tab_role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('tab_role.id')),  # 角色编号
    db.Column('permission_id', db.Integer, db.ForeignKey('tab_permission.id'))  # 权限编号
)


# 菜单表
class Menu(db.Model):
    # 定义表名
    __tablename__ = 'tab_menu'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 用户编号
    name = db.Column(db.String(32))  # 菜单名
    url = db.Column(db.String(32))  # 菜单路径
    parent_id = db.Column(db.Integer)  # 菜单父id，外键本表
    level = db.Column(db.Integer)  # 菜单级别
    permission_id = db.column(db.Integer, db.ForeignKey('tab_permission.id'))  # 关联权限表

    # 将数据转换成 json 格式
    def to_json(self):
        data_json = {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "parent_id": self.parent_id,
            "level": self.level
        }
        return data_json


# 权限和菜单中间表
tab_user_role = db.Table(
    'tab_permission_menu',
    db.Column('permission_id', db.Integer, db.ForeignKey('tab_permission.id')),  # 权限编号
    db.Column('menu_id', db.Integer, db.ForeignKey('tab_menu.id'))  # 菜单编号
)
