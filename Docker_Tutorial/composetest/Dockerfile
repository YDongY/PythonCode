FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
# 安装依赖
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# 对外提供访问端口
EXPOSE 5000
COPY . .
CMD ["flask", "run"]