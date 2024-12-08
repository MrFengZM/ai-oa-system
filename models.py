from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('UserID', db.Integer, primary_key=True, comment='用户ID')
    username = db.Column('Username', db.String(50), unique=True, nullable=False, comment='用户名')
    password_hash = db.Column('PasswordHash', db.String(255), nullable=False, comment='密码哈希')
    email = db.Column('Email', db.String(100), comment='电子邮件')
    phone_number = db.Column('PhoneNumber', db.String(20), comment='电话号码')
    department_id = db.Column('DepartmentID', db.Integer, db.ForeignKey('departments.DepartmentID'), comment='部门ID')
    role_id = db.Column('RoleID', db.Integer, db.ForeignKey('roles.RoleID'), comment='角色ID')
    created_at = db.Column('CreatedAt', db.TIMESTAMP, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column('UpdatedAt', db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 其他模型类（Departments, Roles, Documents, Tasks, Logs）可以根据需要定义