from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# 连接数据库
def get_db_connection():
    """获取数据库连接"""
    return pymysql.connect(
        host=app.config['DB_HOST'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        database=app.config['DB_NAME'],
        port = app.config['DB_PORT'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/register', methods=['POST'])
def register():
    """用户注册接口"""
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': '无效的输入'}), 400

    username = data['username']
    password = data['password']
    email = data.get('email')
    phone_number = data.get('phone_number')

    # 检查用户名是否已存在
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Users WHERE Username=%s"
            cursor.execute(sql, (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                return jsonify({'error': '用户名已存在'}), 400

            # 插入新用户
            password_hash = generate_password_hash(password)
            sql = "INSERT INTO Users (Username, PasswordHash, Email, PhoneNumber) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (username, password_hash, email, phone_number))
            connection.commit()

    return jsonify({'message': '用户注册成功'}), 201

@app.route('/login', methods=['POST'])
def login():
    """用户登录接口"""
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': '无效的输入'}), 400

    username = data['username']
    password = data['password']

    # 查询用户
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Users WHERE Username=%s"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()
            if not user or not check_password_hash(user['PasswordHash'], password):
                return jsonify({'error': '无效的凭据'}), 401

    return jsonify({'message': '登录成功'}), 200

if __name__ == '__main__':
    app.run(debug=True,port=5001)