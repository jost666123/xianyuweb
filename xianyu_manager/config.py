# Configuration file
import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Database configuration
    # 用户需要确保这个数据库是存在的，或者有权限创建它
    # postgresql://username:password@host:port/database_name
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        "postgresql://postgres:nt8j95w5@test-db-postgresql.ns-86pmr0hx.svc:5432/xianyu_data"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Admin credentials
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or "admin"
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or "changeme" # 强烈建议修改这个密码

    # Secret key for session management, CSRF protection, etc.
    # 生成一个随机密钥: import secrets; secrets.token_hex(16)
    SECRET_KEY = os.environ.get('SECRET_KEY') or "a_very_strong_random_secret_key_please_change_me"

    DEBUG = True # 在生产环境中设置为 False

    # Uploads folder
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
