# 使用 Python 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /usr/src/app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


# 复制应用文件到容器中
COPY spider.py ./
COPY databaseLib.py ./
COPY key.py ./
COPY notification.db ./



# 启动 cron 服务和 app.py
CMD ["python", "spider.py"]