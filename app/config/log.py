# app/log.py
import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime


def setup_logger(app):
    log_dir = 'runtime/log'
    # 获取当前日期
    now = datetime.now()
    # 格式化为年和月
    date_path = now.strftime('%Y%m')
    # 日志文件名为当前日期
    log_filename = now.strftime('%d.log')

    # 创建目录路径
    full_log_dir = os.path.join(log_dir, date_path)
    # 如果目录不存在，创建它
    if not os.path.exists(full_log_dir):
        os.makedirs(full_log_dir)

    # 完整日志文件路径
    log_file_path = os.path.join(full_log_dir, log_filename)

    # 设置日志处理器
    handler = RotatingFileHandler(log_file_path, maxBytes=10000, backupCount=3)
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # 添加处理器到Flask的应用日志中
    app.logger.addHandler(handler)
